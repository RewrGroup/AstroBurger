import hashlib


def hash(boxID, tipo_pago, amount, user, orderID):
    coin_name = 'bitcoin'
    public_key = ''
    private_key = ''
    period = ''
    if tipo_pago == 'jugada':
        public_key = '8591AAuVNwoBitcoin77BTCPUBZxyHk5A7YNE0bmy2J3gls6vO'
        private_key = '8591AAuVNwoBitcoin77BTCPRVlBBm1YOY3rLZstduagpNFn6H'
        period = '1 MINUTE'
    elif tipo_pago == 'membresia':
        public_key = '8620AAuGSwaBitcoin77BTCPUBPAxu4lidgnTBTSsmuo694DFv'
        private_key = '8620AAuGSwaBitcoin77BTCPRVYT5IhY8uakoZyYJI2B9umZBW'
        period = '1 MONTH'
    webdev_key = ''
    amountUSD = 0
    language = 'en'
    iframe_id = 'iframe_id'
    user_format = 'MANUAL'
    width = 530
    height = 230
    string = ''
    string = str(boxID) + coin_name + public_key + private_key +webdev_key + str(amount) + period + str(amountUSD)+ language + str(amount) + iframe_id + str(amountUSD) + user + user_format + orderID + str(width) + str(height)
    m = hashlib.md5(string.encode('utf-8'))
    return m.hexdigest()