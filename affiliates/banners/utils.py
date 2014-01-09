from product_details import product_details

def current_firefox_regexp():
        current_firefox = int(product_details.firefox_versions['LATEST_FIREFOX_VERSION'].split('.')[0])
        versions = ['%s' % i for i in range(current_firefox, current_firefox + 4)]
        return '|'.join(versions)
