import ops
import iopc

TARBALL_FILE="weston-4.0.0.tar.xz"
TARBALL_DIR="weston-4.0.0"
INSTALL_DIR="weston-bin"
pkg_path = ""
output_dir = ""
tarball_pkg = ""
tarball_dir = ""
install_dir = ""
install_tmp_dir = ""
cc_host = ""
tmp_include_dir = ""
dst_include_dir = ""
dst_lib_dir = ""
dst_bin_dir = ""

def set_global(args):
    global pkg_path
    global output_dir
    global tarball_pkg
    global install_dir
    global install_tmp_dir
    global tarball_dir
    global cc_host
    global tmp_include_dir
    global dst_include_dir
    global dst_lib_dir
    global dst_bin_dir
    global dst_usr_local_bin_dir
    global dst_usr_local_lib_dir
    global dst_usr_local_libexec_dir
    global dst_usr_local_share_dir
    global dst_pkgconfig_dir
    global install_test_utils
    pkg_path = args["pkg_path"]
    output_dir = args["output_path"]
    tarball_pkg = ops.path_join(pkg_path, TARBALL_FILE)
    install_dir = ops.path_join(output_dir, INSTALL_DIR)
    install_tmp_dir = ops.path_join(output_dir, INSTALL_DIR + "-tmp")
    tarball_dir = ops.path_join(output_dir, TARBALL_DIR)
    cc_host_str = ops.getEnv("CROSS_COMPILE")
    cc_host = cc_host_str[:len(cc_host_str) - 1]
    tmp_include_dir = ops.path_join(output_dir, ops.path_join("include",args["pkg_name"]))
    dst_include_dir = ops.path_join("include",args["pkg_name"])
    dst_bin_dir = ops.path_join(install_dir, "bin")
    dst_lib_dir = ops.path_join(install_dir, "lib")
    dst_usr_local_bin_dir = ops.path_join(install_dir, "usr/local/bin")
    dst_usr_local_lib_dir = ops.path_join(install_dir, "usr/local/lib")
    dst_usr_local_libexec_dir = ops.path_join(install_dir, "usr/local/libexec")
    dst_usr_local_share_dir = ops.path_join(install_dir, "usr/local/share")
    dst_pkgconfig_dir = ops.path_join(ops.path_join(output_dir, "pkgconfig"), "pkgconfig")
    if ops.getEnv("INSTALL_TEST_UTILS") == 'y':
        install_test_utils = True
    else:
        install_test_utils = False

def MAIN_ENV(args):
    set_global(args)

    ops.exportEnv(ops.setEnv("CC", ops.getEnv("CROSS_COMPILE") + "gcc"))
    ops.exportEnv(ops.setEnv("CXX", ops.getEnv("CROSS_COMPILE") + "g++"))
    ops.exportEnv(ops.setEnv("CROSS", ops.getEnv("CROSS_COMPILE")))
    ops.exportEnv(ops.setEnv("DESTDIR", install_tmp_dir))
    #ops.exportEnv(ops.setEnv("PKG_CONFIG_LIBDIR", ops.path_join(iopc.getSdkPath(), "pkgconfig")))
    #ops.exportEnv(ops.setEnv("PKG_CONFIG_SYSROOT_DIR", iopc.getSdkPath()))
    #ops.exportEnv(ops.setEnv("LDFLAGS", ldflags))
    #ops.exportEnv(ops.setEnv("CFLAGS", cflags))
    #ops.exportEnv(ops.setEnv("LIBS", libs))

    return False

def MAIN_EXTRACT(args):
    set_global(args)

    ops.unTarXz(tarball_pkg, output_dir)
    ops.copyto(ops.path_join(pkg_path, "weston_init.sh"), output_dir)

    return True

def MAIN_PATCH(args, patch_group_name):
    set_global(args)
    for patch in iopc.get_patch_list(pkg_path, patch_group_name):
        if iopc.apply_patch(tarball_dir, patch):
            continue
        else:
            sys.exit(1)

    return True

def MAIN_CONFIGURE(args):
    set_global(args)

    cflags = iopc.get_includes()
    libs = iopc.get_libs()

    extra_conf = []
    extra_conf.append("--host=" + cc_host)
    extra_conf.append("--disable-devdocs")
    extra_conf.append("--disable-colord")
    extra_conf.append("--disable-xwayland")
    extra_conf.append("--disable-xwayland-test")
    extra_conf.append("--disable-x11-compositor")
    extra_conf.append("--enable-drm-compositor")
    extra_conf.append("--disable-fbdev-compositor")
    extra_conf.append("--disable-rdp-compositor")
    extra_conf.append("--disable-headless-compositor")
    extra_conf.append("--disable-screen-sharing")
    extra_conf.append("--disable-vaapi-recorder")
    extra_conf.append("--disable-dbus")
    extra_conf.append("--disable-systemd-login")
    extra_conf.append("--disable-junit-xml")
    extra_conf.append("--disable-ivi-shell")
    extra_conf.append("--disable-systemd-notify")
    extra_conf.append("--enable-clients")
    extra_conf.append("--disable-simple-clients")
    extra_conf.append("--enable-weston-launch")
    extra_conf.append("--disable-setuid-install")
    extra_conf.append("--enable-egl")
    extra_conf.append("--disable-wcap-tools")
    extra_conf.append("--enable-simple-egl-clients")
    extra_conf.append("--enable-demo-clients-install")
    #extra_conf.append("--with-host-scanner")
    #extra_conf.append("--disable-documentation")
    extra_conf.append('LIBDRM_CFLAGS=' + cflags)
    extra_conf.append('LIBDRM_LIBS=' + libs)
    extra_conf.append('DRM_COMPOSITOR_CFLAGS=' + cflags)
    extra_conf.append('DRM_COMPOSITOR_LIBS=' + libs)
    extra_conf.append('LIBINPUT_BACKEND_CFLAGS=' + cflags)
    extra_conf.append('LIBINPUT_BACKEND_LIBS=' + libs)
    extra_conf.append('COMPOSITOR_CFLAGS=' + cflags)
    extra_conf.append('COMPOSITOR_LIBS=' + libs)
    extra_conf.append('DRM_COMPOSITOR_GBM_CFLAGS=' + cflags)
    extra_conf.append('DRM_COMPOSITOR_GBM_LIBS=' + libs)
    #extra_conf.append('WAYLAND_PROTOCOLS_CFLAGS="-I' + ops.path_join(iopc.getSdkPath(), 'usr/include/wayland') + '"')
    #extra_conf.append('WAYLAND_PROTOCOLS_LIBS="-L' + ops.path_join(iopc.getSdkPath(), 'lib') + '"')
    extra_conf.append('WAYLAND_COMPOSITOR_CFLAGS=' + cflags)
    extra_conf.append('WAYLAND_COMPOSITOR_LIBS=' + libs)
    extra_conf.append('PIXMAN_CFLAGS=' + cflags)
    extra_conf.append('PIXMAN_LIBS=' + libs)
    extra_conf.append('PNG_CFLAGS=' + cflags)
    extra_conf.append('PNG_LIBS=' + libs)
    extra_conf.append('CAIRO_CFLAGS=' + cflags)
    extra_conf.append('CAIRO_LIBS=' + libs)
    extra_conf.append('TEST_CLIENT_CFLAGS=' + cflags)
    extra_conf.append('TEST_CLIENT_LIBS=' + libs)
    extra_conf.append('CLIENT_CFLAGS=' + cflags)
    extra_conf.append('CLIENT_LIBS=' + libs)
    extra_conf.append('SERVER_CFLAGS=' + cflags)
    extra_conf.append('SERVER_LIBS=' + libs)
    extra_conf.append('WESTON_INFO_CFLAGS=' + cflags)
    extra_conf.append('WESTON_INFO_LIBS=' + libs)
    extra_conf.append('XKBCOMMON_COMPOSE_CFLAGS=' + cflags)
    extra_conf.append('XKBCOMMON_COMPOSE_LIBS=' + libs)
    extra_conf.append('EGL_CFLAGS=' + cflags) 
    extra_conf.append('EGL_LIBS=' + libs)
    extra_conf.append('EGL_TESTS_CFLAGS=' + cflags)
    extra_conf.append('EGL_TESTS_LIBS=' + libs)
    extra_conf.append('WAYLAND_COMPOSITOR_EGL_CFLAGS=' + cflags)
    extra_conf.append('WAYLAND_COMPOSITOR_EGL_LIBS=' + libs)
    extra_conf.append('SIMPLE_EGL_CLIENT_CFLAGS=' + cflags)
    extra_conf.append('SIMPLE_EGL_CLIENT_LIBS=' + libs)
    iopc.configure(tarball_dir, extra_conf)

    return True

def MAIN_BUILD(args):
    set_global(args)

    extra_conf = []
    extra_conf.append("V=1")
    ops.mkdir(install_dir)
    ops.mkdir(install_tmp_dir)
    iopc.make(tarball_dir, extra_conf)
    iopc.make_install(tarball_dir)

    ops.mkdir(install_dir)
    ops.mkdir(dst_lib_dir)
    ops.mkdir(dst_bin_dir)
    ops.mkdir(dst_usr_local_bin_dir)
    ops.mkdir(dst_usr_local_lib_dir)
    ops.mkdir(dst_usr_local_libexec_dir)
    ops.mkdir(dst_usr_local_share_dir)
    ops.mkdir(dst_pkgconfig_dir)


    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/bin/weston"), dst_usr_local_bin_dir)
    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/bin/weston-launch"), dst_usr_local_bin_dir)
    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/bin/weston-terminal"), dst_usr_local_bin_dir)
    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/bin/weston-info"), dst_usr_local_bin_dir)
    ops.copyto(ops.path_join(output_dir, "weston_init.sh"), dst_bin_dir)

    if install_test_utils :
        ops.copyto(ops.path_join(install_tmp_dir, "usr/local/bin/weston-calibrator"), dst_usr_local_bin_dir)
        ops.copyto(ops.path_join(install_tmp_dir, "usr/local/bin/weston-clickdot"), dst_usr_local_bin_dir)
        ops.copyto(ops.path_join(install_tmp_dir, "usr/local/bin/weston-cliptest"), dst_usr_local_bin_dir)
        ops.copyto(ops.path_join(install_tmp_dir, "usr/local/bin/weston-confine"), dst_usr_local_bin_dir)
        ops.copyto(ops.path_join(install_tmp_dir, "usr/local/bin/weston-dnd"), dst_usr_local_bin_dir)
        ops.copyto(ops.path_join(install_tmp_dir, "usr/local/bin/weston-eventdemo"), dst_usr_local_bin_dir)
        ops.copyto(ops.path_join(install_tmp_dir, "usr/local/bin/weston-flower"), dst_usr_local_bin_dir)
        ops.copyto(ops.path_join(install_tmp_dir, "usr/local/bin/weston-fullscreen"), dst_usr_local_bin_dir)
        ops.copyto(ops.path_join(install_tmp_dir, "usr/local/bin/weston-image"), dst_usr_local_bin_dir)
        ops.copyto(ops.path_join(install_tmp_dir, "usr/local/bin/weston-resizor"), dst_usr_local_bin_dir)
        ops.copyto(ops.path_join(install_tmp_dir, "usr/local/bin/weston-scaler"), dst_usr_local_bin_dir)
        ops.copyto(ops.path_join(install_tmp_dir, "usr/local/bin/weston-simple-egl"), dst_usr_local_bin_dir)
        ops.copyto(ops.path_join(install_tmp_dir, "usr/local/bin/weston-smoke"), dst_usr_local_bin_dir)
        ops.copyto(ops.path_join(install_tmp_dir, "usr/local/bin/weston-stacking"), dst_usr_local_bin_dir)
        ops.copyto(ops.path_join(install_tmp_dir, "usr/local/bin/weston-subsurfaces"), dst_usr_local_bin_dir)
        ops.copyto(ops.path_join(install_tmp_dir, "usr/local/bin/weston-transformed"), dst_usr_local_bin_dir)

    libweston = "libweston-4.so.0.0.0"
    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/lib/" + libweston), dst_lib_dir)
    ops.ln(dst_lib_dir, libweston, "libweston-4.so.0.0")
    ops.ln(dst_lib_dir, libweston, "libweston-4.so.0")
    ops.ln(dst_lib_dir, libweston, "libweston-4.so")

    libweston_desktop = "libweston-desktop-4.so.0.0.0"
    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/lib/" + libweston_desktop), dst_lib_dir)
    ops.ln(dst_lib_dir, libweston_desktop, "libweston-desktop-4.so.0.0")
    ops.ln(dst_lib_dir, libweston_desktop, "libweston-desktop-4.so.0")
    ops.ln(dst_lib_dir, libweston_desktop, "libweston-desktop-4.so")

    libweston_dir = ops.path_join(dst_usr_local_lib_dir, "libweston-4")
    ops.mkdir(libweston_dir)
    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/lib/libweston-4/wayland-backend.so"), libweston_dir)
    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/lib/libweston-4/drm-backend.so"), libweston_dir)
    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/lib/libweston-4/gl-renderer.so"), libweston_dir)

    libweston_dir = ops.path_join(dst_usr_local_lib_dir, "weston")
    ops.mkdir(libweston_dir)
    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/lib/weston/desktop-shell.so"), libweston_dir)
    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/lib/weston/fullscreen-shell.so"), libweston_dir)

    ops.mkdir(dst_usr_local_share_dir)

    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/share/wayland-sessions"), dst_usr_local_share_dir)
    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/share/weston"), dst_usr_local_share_dir)

    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/libexec/."), dst_usr_local_libexec_dir)

    ops.mkdir(tmp_include_dir)
    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/include/."), tmp_include_dir)
    return True

def MAIN_INSTALL(args):
    set_global(args)

    iopc.installBin(args["pkg_name"], ops.path_join(ops.path_join(install_dir, "bin"), "."), "bin")
    iopc.installBin(args["pkg_name"], ops.path_join(ops.path_join(install_dir, "lib"), "."), "lib")
    iopc.installBin(args["pkg_name"], ops.path_join(dst_usr_local_bin_dir, "."), "usr/local/bin")
    iopc.installBin(args["pkg_name"], ops.path_join(dst_usr_local_share_dir, "."), "usr/local/share")
    iopc.installBin(args["pkg_name"], ops.path_join(dst_usr_local_lib_dir, "."), "usr/local/lib")
    iopc.installBin(args["pkg_name"], ops.path_join(dst_usr_local_libexec_dir, "."), "usr/local/libexec")
    iopc.installBin(args["pkg_name"], ops.path_join(tmp_include_dir, "."), dst_include_dir)
    iopc.installBin(args["pkg_name"], ops.path_join(dst_pkgconfig_dir, '.'), "pkgconfig")

    return False

def MAIN_SDKENV(args):
    set_global(args)

    cflags = ""
    cflags += " -I" + ops.path_join(iopc.getSdkPath(), 'usr/include/' + args["pkg_name"])
    iopc.add_includes(cflags)

    libs = ""
    libs += " -lweston-4 -lweston-desktop-4"
    iopc.add_libs(libs)

    return False

def MAIN_CLEAN_BUILD(args):
    set_global(args)

    return False

def MAIN(args):
    set_global(args)

