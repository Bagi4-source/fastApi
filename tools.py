import argostranslate.package
import argostranslate.translate

AP = argostranslate.package.get_available_packages()
available_packages = [(x.from_code, x.to_code) for x in AP]


def install(from_code, to_code):
    if (from_code, to_code) not in available_packages:
        return
    installed_packages = [(x.from_code, x.to_code) for x in argostranslate.package.get_installed_packages()]
    if (from_code, to_code) not in installed_packages:
        try:
            package_to_install = next(
                filter(
                    lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
                )
            )
            argostranslate.package.install_from_path(package_to_install.download())
        except Exception as e:
            logging.error(f'[INSTALL]: {e}')
            return
    return True
