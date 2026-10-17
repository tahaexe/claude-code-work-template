#!/usr/bin/env python3
"""Check that R8 kept every Java class the game names from C# or native code.

C# (through AndroidJavaClass/Object/Proxy) and native libraries (JNI FindClass)
reach Java classes by name, which R8 can't see: without a keep rule it renames
or removes them, and the game fails only at runtime on a device
(ClassNotFoundException, NoSuchMethodError). This script reads a built AAB or APK:
1. names from C#: string literals in IL2CPP's global-metadata.dat
   (metadata v38+ layout, plus the older (length, index) layout);
2. names from native code: JNI class strings in lib/<abi>/*.so (arm64-v8a, else
   x86_64: the BlueStacks check APK);
3. the classes defined in the DEX files (an AAB's base/dex/, an APK's classes*.dex).
A named class is MISSING when the DEX doesn't define it (renamed or removed)
and ALLOWED doesn't explain it. C# names count even when their whole package is
absent: R8 removes a whole library that no Java code calls (Project B's Play
In-app Review, found 2026-10-10). Names only native code uses whose package is
absent are just counted: Firebase's C++ layer names every Firebase product.
REQUIRED classes are those Java code loads by reflection (nothing names them), with
the methods it calls: WorkManager's Room database is built from WorkDatabase_Impl's
constructor, and without it every launch crashes (a project's closure review, 2026-10-15).
An EXPECTED assembly that is in the build (ScriptingAssemblies.json) while C# no longer
names its class is STRIPPED: managed code stripping removed that C# path; counted as missing.
Template copy (1.51) of a project's tool (2026-10-16), grown from four other projects' copies
(IAP 5.4 allowances; APKs, REQUIRED methods); --compare by defined methods
(2026-10-16, below). Its allow lists keep only SDK-level reasons: a project adds its own, each with a
reason, and keeps them when it takes a newer template copy (handbook google-play-level-up.md, section 9).

Usage:
  python r8-kontrol.py <aab|apk>                # exit 1 if a named class is missing
  python r8-kontrol.py -v <aab|apk>             # also list the allowed names found
  python r8-kontrol.py --compare <old> <new>    # also: no callable method lost on named classes

  python r8-kontrol.py --compare <old> <new> --bundletool <bundletool-all.jar>
                                                # also: no resource removed by shrinking (AABs)

--compare flags a method of a named class that the old build had and the new one lacks
when it is a constructor or its name appears in C# literals or in those native libraries'
strings (callable by name); obfuscated internals (zza…) are only counted. "Had" means
defined by the class, or called through it in the old DEX and defined by a superclass
there; "lacks" means neither the class nor a superclass in the new DEX defines it (JNI
finds methods through the superclasses). So a framework method the old DEX called through
the class (GameActivity.getAssets, an enum's ordinal) is no loss when R8 rebinds the call
to the defining class (Project E's first R8 bundle: 13 such false alarms, 2026-10-16).
A lost class or method may be allowed, with a reason.
--bundletool lists the resource entries both bundles define (`bundletool dump resources`,
run with the JDK next to the jar in a Unity install, else `java` on PATH) and flags each one
the new bundle lost: code may read it by name (getIdentifier), which shrinking can't see.
Keep such resources with a res/raw keep file in an .androidlib under Assets/Plugins/Android/
(e.g. a project's KeepResources.androidlib).
"""
import json
import os
import re
import struct
import subprocess
import sys
import zipfile

CLASS_DOT = re.compile(r'^(?:com|androidx|org|io|dalvik)(?:\.[A-Za-z0-9_]+)+\.[A-Z][A-Za-z0-9_]*(?:\$[A-Za-z0-9_]+)*$')
CLASS_SLASH = re.compile(rb'(?:com|androidx|org|io)(?:/[A-Za-z0-9_]+)+/[A-Z][A-Za-z0-9_]*(?:\$[A-Za-z0-9_]+)*')

# Named but deliberately absent; each needs a reason.
ALLOWED = {
    'com.google.android.gms.ads.AdRequest$Builder': 'legacy Google Mobile Ads path; the game uses the Next-Gen SDK (selectedGmaAndroidSdk 1, since 8.1)',
    'com.google.android.gms.ads.RequestConfiguration$Builder': 'legacy Google Mobile Ads path (Next-Gen SDK in use)',
    'com.google.android.gms.ads.RequestConfiguration$PublisherPrivacyPersonalizationState': 'legacy Google Mobile Ads path (Next-Gen SDK in use)',
    'com.google.android.gms.ads.rewarded.ServerSideVerificationOptions$Builder': 'legacy Google Mobile Ads path (Next-Gen SDK in use)',
    # Legacy SDK (play-services-ads) classes: the build has only ads-mobile-sdk 1.3.1, so they were
    # never in it (not removed by R8); flagged once C# names counted with their package absent (2026-10-10).
    'com.google.ads.mediation.admob.AdMobAdapter': 'legacy Google Mobile Ads path (Next-Gen SDK in use)',
    'com.google.android.gms.ads.admanager.AdManagerAdRequest$Builder': 'legacy Google Mobile Ads path (Next-Gen SDK in use)',
    'com.google.android.gms.ads.initialization.AdapterStatus$State': 'legacy Google Mobile Ads path (Next-Gen SDK in use)',
    'com.google.android.gms.ads.initialization.OnInitializationCompleteListener': 'legacy Google Mobile Ads path (Next-Gen SDK in use)',
    'com.google.android.gms.ads.preload.PreloadCallback': 'legacy Google Mobile Ads path (Next-Gen SDK in use)',
    'com.google.android.gms.ads.preload.PreloadConfiguration$Builder': 'legacy Google Mobile Ads path (Next-Gen SDK in use)',
    # Play Core plugin 1.8.6's old task proxies (PlayCoreOnSuccessListener/OnFailureListener): nothing creates them,
    # yet their names stay in IL2CPP metadata; play:core-common 2.x has no such package, and the review plugin
    # uses com.google.android.gms.tasks (2026-10-12).
    'com.google.android.play.core.tasks.OnFailureListener': 'unused legacy Play Core proxy; reviews use gms tasks',
    'com.google.android.play.core.tasks.OnSuccessListener': 'unused legacy Play Core proxy; reviews use gms tasks',
    # Unity IAP 5.4.2 (Project G, 2026-10-12): Resources paths that match the class-name pattern.
    'com.unity.purchasing.Brands.AppleInAppPurchase1ln': 'not a Java class: IAP 5.4.2 Resources sprite path (PaymentBrandRegistry, "com.unity.purchasing/Brands/...")',
    'com.unity.purchasing.Brands.AppleInAppPurchase1lnWhite': 'not a Java class: IAP 5.4.2 Resources sprite path (PaymentBrandRegistry, "com.unity.purchasing/Brands/...")',
    'com.unity.purchasing.Brands.Coda': 'not a Java class: IAP 5.4.2 Resources sprite path (PaymentBrandRegistry, "com.unity.purchasing/Brands/...")',
    'com.unity.purchasing.Brands.CodaWhite': 'not a Java class: IAP 5.4.2 Resources sprite path (PaymentBrandRegistry, "com.unity.purchasing/Brands/...")',
    'com.unity.purchasing.Brands.GooglePlayWordmark': 'not a Java class: IAP 5.4.2 Resources sprite path (PaymentBrandRegistry, "com.unity.purchasing/Brands/...")',
    'com.unity.purchasing.Brands.GooglePlayWordmarkWhite': 'not a Java class: IAP 5.4.2 Resources sprite path (PaymentBrandRegistry, "com.unity.purchasing/Brands/...")',
    'com.unity.purchasing.Brands.StripeWhite': 'not a Java class: IAP 5.4.2 Resources sprite path (PaymentBrandRegistry, "com.unity.purchasing/Brands/...")',
    'com.unity.purchasing.Brands.Webshop': 'not a Java class: IAP 5.4.2 Resources sprite path (PaymentBrandRegistry, "com.unity.purchasing/Brands/...")',
    'com.unity.purchasing.Brands.WebshopWhite': 'not a Java class: IAP 5.4.2 Resources sprite path (PaymentBrandRegistry, "com.unity.purchasing/Brands/...")',
    'com.unity.purchasing.PaymentOptionProviderModal': 'not a Java class: IAP 5.4.2 USS Resources path (PaymentOptionProviderUITK)',
    'com.unity.purchasing.common.IUnityCallback': 'IAP 5.4.2 JavaBridge proxy interface; nothing in the package constructs JavaBridge (unused path)',
    # Project entries go below, each with its reason. Seen in practice: a Play Asset Delivery plugin in
    # Assets/GooglePlayPlugins that no game code calls; Play package ids in C# (a "More Games" list) that match the
    # class-name pattern but are never loaded as classes.
}
# Classes that Java code loads by name, so nothing in C# or the native libraries names them: they must be in the
# DEX (AdMob loads a mediation adapter by the class name in its server config; plan gelir-paketi-4, 2026-10-12).
# Checked when the trigger assembly is in the build or a class with the trigger prefix is in the DEX (EDM ships the
# Java adapter without the C# wiring too); the listed methods must be in the class as well.
REQUIRED = {
    'com.google.ads.mediation.unity.UnityMediationAdapter': (('GoogleMobileAds.Mediation.UnityAds.Android.dll', 'com.unity3d.ads.'),
                                                             'AdMob mediation loads the Unity Ads adapter by name', ()),
    # The ads SDK brings WorkManager; Room creates its database by reflection on the generated class's constructor,
    # which R8's full mode drops without a keep rule ("Failed to create an instance of WorkDatabase" at every launch).
    'androidx.work.impl.WorkDatabase_Impl': ((None, 'androidx.work.impl.'),
                                             'Room builds WorkManager\'s database by reflection', ('<init>',)),
}
# Classes C# must name when an assembly is in the build: a missing name means managed code stripping removed
# that C# path (the self-registering Play review backend, until [assembly: AlwaysLinkAssembly], 2026-10-12).
# Example entry: a self-registering review assembly; checked only when that assembly is in the build.
EXPECTED = {
    # 'Studio.Review.Play.dll': 'com.google.android.play.core.review.ReviewManagerFactory',
}
# Methods of named classes that may go; each needs a reason.
ALLOWED_LOST = {
    ('com.google.android.ump.UserMessagingPlatform', '<init>'): 'static utility class; the plugin calls only its static methods',
    # Project E's first R8 bundle vs 1.0 (2) (2026-10-16): another project (same SDKs) ships the same result and ran
    # clean on an emulator; a third (R8 on, live) lacks the Google Mobile Ads ones too. A game without native
    # ads also loses the Next-Gen SDK's NativeAd$NativeAdType and NativeAd$NativeMediaAspectRatio constructors:
    # allow them in the project, with that reason.
    ('com.google.android.gms.ads.AdFormat', '<init>'): 'legacy Google Mobile Ads path (Next-Gen SDK in use); nothing constructs an enum by name',
    ('com.google.android.libraries.ads.mobile.sdk.MobileAds', 'stop'): 'the GMA plugin\'s C# has no "stop" literal: the name comes from other code',
    ('com.google.android.gms.common.api.Status', 'isCanceled'): 'Firebase C++ calls isCanceled on gms Task; it names Status only in Storage\'s signature (Storage not in the build)',
    ('com.google.androidgamesdk.GameActivity', 'getAbsolutePath'): 'its private static helper for onCreate\'s paths (no JNI caller); the name in native strings is java.io.File\'s',
}
# Named classes that may go entirely; each needs a reason.
ALLOWED_LOST_CLASSES = {
    'com.google.protobuf.ByteString': 'named only in Firestore Blob\'s JNI signature in Firebase\'s combined C++ library; Firestore is not in the build',
}
# Resource entries that shrinking may remove; each needs a reason. Styleables (attribute
# arrays, not runtime resources) are skipped.
ALLOWED_REMOVED = {
    'raw/firebase_common_keep': 'keep-rule file read by the shrinker, unused at runtime',
    'raw/firebase_crashlytics_keep': 'keep-rule file read by the shrinker, unused at runtime',
    'bool/abc_allow_stacked_button_bar': 'AppCompat dialog internals, not read by name',
}
IDENT = re.compile(rb'[A-Za-z_][A-Za-z0-9_]{3,}')


def il2cpp_literals(data):
    sanity, version = struct.unpack_from('<Ii', data, 0)
    if sanity != 0xFAB11BAF:
        raise ValueError('not an IL2CPP global-metadata.dat')
    if version >= 38:
        # Sections are (offset, size, count). A literal entry is its start index in the
        # data section; the next entry's index ends it (the last entry is the end).
        lit_off, _, lit_count = struct.unpack_from('<iii', data, 8)
        dat_off, dat_size, _ = struct.unpack_from('<iii', data, 20)
        starts = struct.unpack_from('<%dI' % lit_count, data, lit_off)
        if list(starts) != sorted(starts) or starts[-1] > dat_size:
            raise ValueError('unexpected metadata v%d literal table' % version)
        return [data[dat_off + a:dat_off + b].decode('utf-8', 'replace') for a, b in zip(starts, starts[1:])]
    # Older layouts: (offset, size) pairs or triples; entries are (length, index).
    for stride in (8, 12):
        lit_off, lit_size = struct.unpack_from('<ii', data, 8)
        dat_off, dat_size = struct.unpack_from('<ii', data, 8 + stride)
        if lit_size % 8 or not (0 < lit_off < len(data)) or not (0 < dat_off < len(data)):
            continue
        out = []
        for i in range(lit_size // 8):
            length, index = struct.unpack_from('<Ii', data, lit_off + 8 * i)
            if index < 0 or index + length > dat_size:
                break
            out.append(data[dat_off + index:dat_off + index + length].decode('utf-8', 'replace'))
        else:
            return out
    raise ValueError('unknown metadata layout, version %d' % version)


def uleb(data, pos):
    result = shift = 0
    while True:
        b = data[pos]
        pos += 1
        result |= (b & 0x7F) << shift
        if b < 0x80:
            return result, pos
        shift += 7


def dex_classes(dex):
    """({class name: set of the method names it defines}, {class name: its superclass},
    {type name: set of the method names the DEX refers to through that type}) for one DEX."""
    s_size, s_off, t_size, t_off = struct.unpack_from('<IIII', dex, 0x38)
    m_size, m_off, c_size, c_off = struct.unpack_from('<IIII', dex, 0x58)

    def string(i):
        (data_off,) = struct.unpack_from('<I', dex, s_off + 4 * i)
        _, p = uleb(dex, data_off)
        return dex[p:dex.index(b'\0', p)].decode('utf-8', 'replace')

    types = [struct.unpack_from('<I', dex, t_off + 4 * i)[0] for i in range(t_size)]
    cache = {}

    def type_name(ti):
        if ti not in cache:
            d = string(types[ti])
            cache[ti] = d[1:-1].replace('/', '.') if d.startswith('L') else d
        return cache[ti]

    def method_name(i):
        _, _, name_idx = struct.unpack_from('<HHI', dex, m_off + 8 * i)
        return string(name_idx)

    referenced = {}
    for i in range(m_size):
        cls_idx, _, name_idx = struct.unpack_from('<HHI', dex, m_off + 8 * i)
        referenced.setdefault(type_name(cls_idx), set()).add(string(name_idx))
    # class_def_item: class, access, superclass, interfaces, source file, annotations, class_data, static values.
    defined, supers = {}, {}
    for i in range(c_size):
        cls_idx, _, super_idx, _, _, _, data_off, _ = struct.unpack_from('<8I', dex, c_off + 32 * i)
        name = type_name(cls_idx)
        supers[name] = type_name(super_idx) if super_idx != 0xFFFFFFFF else None
        methods = defined[name] = set()
        if not data_off:
            continue
        counts, p = [], data_off  # class_data_item: static and instance fields, direct and virtual methods
        for _ in range(4):
            n, p = uleb(dex, p)
            counts.append(n)
        for _ in range(counts[0] + counts[1]):  # field: index diff, access flags
            _, p = uleb(dex, p)
            _, p = uleb(dex, p)
        for n in counts[2:]:  # method: index diff (from 0 in each list), access flags, code offset
            index = 0
            for _ in range(n):
                diff, p = uleb(dex, p)
                _, p = uleb(dex, p)
                _, p = uleb(dex, p)
                index += diff
                methods.add(method_name(index))
    return defined, supers, referenced


def is_class_name(name):
    # An ALL_CAPS last part is a constant or meta-data key, not a class.
    return CLASS_DOT.match(name) and not re.fullmatch(r'[A-Z0-9_]+', name.rsplit('.', 1)[1])


def layout(z):
    """(prefix of the base module, the DEX file names, the ABI whose native libraries are read)."""
    names = z.namelist()
    prefix = 'base/' if 'base/manifest/AndroidManifest.xml' in names else ''
    if prefix:
        dexes = [n for n in names if n.startswith('base/dex/') and n.endswith('.dex')]
    else:
        dexes = [n for n in names if re.fullmatch(r'classes\d*\.dex', n)]
    abis = {n.split('/')[-2] for n in names if n.startswith(prefix + 'lib/') and n.endswith('.so')}
    abi = next((a for a in ('arm64-v8a', 'x86_64', 'armeabi-v7a') if a in abis), None)
    return prefix, dexes, abi


def named_classes(z):
    """({class name: set of sources}, set of names that code could call by name)."""
    refs, callable_names = {}, set()
    prefix, _, abi = layout(z)
    for n in z.namelist():
        if n.endswith('global-metadata.dat'):
            for s in il2cpp_literals(z.read(n)):
                s = s.strip()
                if re.fullmatch(r'[A-Za-z_$][A-Za-z0-9_$]*', s):
                    callable_names.add(s)
                s = s.replace('/', '.')
                if is_class_name(s):
                    refs.setdefault(s, set()).add('C#')
        elif n.endswith('.so') and n.startswith('%slib/%s/' % (prefix, abi)):
            data = z.read(n)
            found = False
            for m in CLASS_SLASH.findall(data):
                s = m.decode().replace('/', '.')
                if is_class_name(s):
                    refs.setdefault(s, set()).add(n.rsplit('/', 1)[1])
                    found = True
            if found:
                callable_names.update(m.decode() for m in IDENT.findall(data))
    return refs, callable_names


def load(aab):
    z = zipfile.ZipFile(aab)
    prefix, dexes, abi = layout(z)
    classes, supers, referenced, dex_bytes = {}, {}, {}, 0
    for n in dexes:
        data = z.read(n)
        dex_bytes += len(data)
        defined, parents, uses = dex_classes(data)
        classes.update(defined)
        supers.update(parents)
        for c, methods in uses.items():
            referenced.setdefault(c, set()).update(methods)
    stats = {}
    if 'BUNDLE-METADATA/com.android.tools/r8.json' in z.namelist():
        stats = json.loads(z.read('BUNDLE-METADATA/com.android.tools/r8.json')).get('stats', {})
    res = sum(1 for n in z.namelist() if n.startswith(prefix + 'res/'))
    refs, callable_names = named_classes(z)
    return z, classes, refs, callable_names, dex_bytes, stats, res, (supers, referenced)


def check(aab, verbose=False):
    z, classes, refs, _, dex_bytes, stats, res, _ = load(aab)
    prefix, dexes, abi = layout(z)
    packages = {c.rsplit('.', 1)[0] for c in classes}
    missing = allowed = present = native_only = 0
    for c in sorted(refs):
        if c in classes:
            present += 1
        elif c in ALLOWED:
            allowed += 1
            if verbose:
                print('ALLOWED  %s  (%s)' % (c, ALLOWED[c]))
        elif c.rsplit('.', 1)[0] not in packages and 'C#' not in refs[c]:
            native_only += 1
        else:
            missing += 1
            print('MISSING  %s  (named by %s)' % (c, ', '.join(sorted(refs[c]))))
    listed = prefix + 'assets/bin/Data/ScriptingAssemblies.json'
    assemblies = set(json.loads(z.read(listed)).get('names', [])) if listed in z.namelist() else set()
    for c, ((asm, sdk), reason, methods) in sorted(REQUIRED.items()):
        if not ((asm and asm in assemblies) or any(k.startswith(sdk) for k in classes)):
            continue
        if c not in classes:
            missing += 1
            print('MISSING  %s  (%s)' % (c, reason))
        elif any(m not in classes[c] for m in methods):
            missing += 1
            print('MISSING  %s.%s  (%s)' % (c, '/'.join(m for m in methods if m not in classes[c]), reason))
        elif verbose:
            print('REQUIRED present  %s %s' % (c, ' '.join(methods)))
    for asm, c in sorted(EXPECTED.items()):
        if asm in assemblies and 'C#' not in refs.get(c, ()):
            missing += 1
            print('STRIPPED  %s is in the build, but C# no longer names %s' % (asm, c))
    print('%s: %s, %d DEX files %.2f MB, %d classes, native %s, res files %d; R8 no-obfuscation %s%%, no-shrinking %s%%'
          % (aab.replace('\\', '/').rsplit('/', 1)[-1], 'AAB' if prefix else 'APK', len(dexes), dex_bytes / 1e6,
             len(classes), abi, res, stats.get('noObfuscationPercentage', '?'), stats.get('noShrinkingPercentage', '?')))
    print('named %d: present %d, missing %d, allowed %d, native-only with package absent %d'
          % (len(refs), present, missing, allowed, native_only))
    return missing


def callable_methods(c, classes, supers):
    """What JNI finds on c by name: the methods c defines and those its superclasses in the DEX define (constructors
    only c's own). A framework superclass is never in the DEX, and R8 can't remove what it defines."""
    found, k = set(classes[c]), supers.get(c)
    while k in classes:
        found |= classes[k] - {'<init>', '<clinit>'}
        k = supers.get(k)
    return found


def compare(old, new, verbose=False):
    _, old_classes, old_refs, old_names, *_, (old_supers, old_uses) = load(old)
    _, new_classes, new_refs, new_names, *_, (new_supers, _) = load(new)
    names = old_names | new_names
    lost = internal = allowed = 0
    for c in sorted(set(old_refs) | set(new_refs)):
        if c not in old_classes:
            continue
        if c not in new_classes:
            if c in ALLOWED_LOST_CLASSES:
                allowed += 1
                if verbose:
                    print('ALLOWED LOST CLASS  %s  (%s)' % (c, ALLOWED_LOST_CLASSES[c]))
                continue
            lost += 1
            print('LOST CLASS  %s' % c)
            continue
        # Judged: what c defines, and what the old DEX called through c that a superclass in the DEX defines
        # (a superclass's other members, often obfuscated, are its own business).
        judged = old_classes[c] | (old_uses.get(c, set()) & callable_methods(c, old_classes, old_supers))
        gone = judged - callable_methods(c, new_classes, new_supers)
        named = sorted(m for m in gone if m == '<init>' or m in names)
        bad = [m for m in named if (c, m) not in ALLOWED_LOST]
        internal += len(gone) - len(named)
        allowed += len(named) - len(bad)
        if verbose:
            for m in named:
                if (c, m) in ALLOWED_LOST:
                    print('ALLOWED LOST  %s.%s  (%s)' % (c, m, ALLOWED_LOST[(c, m)]))
        if bad:
            lost += 1
            print('LOST METHODS  %s: %s' % (c, ', '.join(bad)))
    print('compare: %d named classes lost a class or callable methods (%d allowed, %d internal methods dropped)'
          % (lost, allowed, internal))
    return lost


def resource_entries(aab, jar):
    java = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(jar))), 'OpenJDK', 'bin', 'java.exe')
    if not os.path.exists(java):
        java = 'java'
    out = subprocess.run([java, '-Xmx512m', '-jar', jar, 'dump', 'resources', '--bundle', aab],
                         capture_output=True, text=True, check=True).stdout
    return {m.group(1) for m in re.finditer(r'^0x[0-9a-f]+ - (\S+)', out, re.M)}


def compare_resources(old, new, jar):
    removed = sorted(r for r in resource_entries(old, jar) - resource_entries(new, jar)
                     if not r.startswith('styleable/'))
    bad = [r for r in removed if r not in ALLOWED_REMOVED]
    for r in bad:
        print('REMOVED RESOURCE  %s' % r)
    print('resources: %d entries removed, %d not allowed' % (len(removed), len(bad)))
    return len(bad)


def main(argv):
    jar = None
    verbose = '-v' in argv
    argv = [a for a in argv if a != '-v']
    if '--bundletool' in argv:
        i = argv.index('--bundletool')
        jar = argv[i + 1]
        argv = argv[:i] + argv[i + 2:]
    if len(argv) == 3 and argv[0] == '--compare':
        check(argv[1])  # the old build is shown, not judged
        bad = check(argv[2], verbose) + compare(argv[1], argv[2], verbose)
        if jar:
            bad += compare_resources(argv[1], argv[2], jar)
        return 1 if bad else 0
    if len(argv) == 1:
        return 1 if check(argv[0], verbose) else 0
    print(__doc__)
    return 2


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
