import hashlib


def hash(boxID, tipo_pago, amount, user, orderID):
    # boxID = 8591
    coin_name = 'bitcoin'
    public_key = ''
    private_key = ''
    period = ''
    if tipo_pago == 'jugada':
        public_key = '8591AAuVNwoBitcoin77BTCPUBZxyHk5A7YNE0bmy2J3gls6vO'
        private_key = '8591AAuVNwoBitcoin77BTCPRVlBBm1YOY3rLZstduagpNFn6H'
        period = '1 MINUTE'
    elif tipo_pago == 'membresia':
        public_key = 'la-clave-para-las-membresias'
        private_key = 'la-clave-para-las-membresias'
        period = '1 MONTH'
    webdev_key = ''
    amountUSD = 0
    # period = '1 MINUTE'
    # amount_usd = 0.6
    language = 'en'
    iframe_id = 'iframe_id'
    # userid = 'betcnow'
    user_format = 'MANUAL'
    # order_id = 'product1'
    width = 530
    height = 230
    string = ''
    string = str(boxID) + coin_name + public_key + private_key +webdev_key + str(amount) + period + str(amountUSD)+ language + str(amount) + iframe_id + str(amountUSD) + user + user_format + orderID + str(width) + str(height)
    m = hashlib.md5(string.encode('utf-8'))
    return m.hexdigest()