import xrpl

class XRPLClient:
    def __init__(self, xrpl_net_url: str):
        self.client = xrpl.clients.JsonRpcClient(xrpl_net_url)

    def get_account(self, seed: str):
        """get_account"""
        if (seed == ''):
            new_wallet = xrpl.wallet.generate_faucet_wallet(self.client)
        else:
            new_wallet = xrpl.wallet.Wallet.from_seed(seed)
        return new_wallet
    
    def get_account_info(self, account_id: str):
        """get_account_info"""
        acct_info = xrpl.models.request.account_info.AccountInfo(
            account=account_id,
            ledger_index="validated"
        )
        response = self.client(acct_info)
        return response.result['account_data']
    
    def send_xrp(self, seed, amount, destination):
        """send_xrp"""
        sending_wallet = xrpl.wallet.Wallet.from_seed(seed)
        payment = xrpl.models.transaction.Payment(
            account=sending_wallet.address,
            amount=xrpl.utils.xrp_to_drops(int(amount)),
            destination=destination
        )
        try:
            response = xrpl.transaction.submit_and_wait(payment, self.client, sending_wallet)
        except xrpl.transaction.XRPLReliableSubmissionException as e:
            response = f"Submit failed: {e}"
        return response