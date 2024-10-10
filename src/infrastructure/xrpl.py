import xrpl.clients
import xrpl.wallet
import xrpl.transaction
import xrpl.utils

class XRPLClient:
    def __init__(self, xrpl_net_url: str):
        self.client = xrpl.clients.JsonRpcClient(xrpl_net_url)

    async def get_account(self, seed: str = None):
        """Generate a new wallet or return an existing wallet from seed"""
        if not seed:
            new_wallet = xrpl.wallet.generate_faucet_wallet(self.client)
        else:
            new_wallet = xrpl.wallet.Wallet.from_seed(seed)
        return new_wallet
    
    async def get_account_info(self, account_id: str):
        """Fetch account information from the ledger"""
        acct_info = xrpl.models.request.account_info.AccountInfo(
            account=account_id,
            ledger_index="validated"
        )
        response = self.client.request(acct_info)
        return response.result.get('account_data', None)
    
    async def send_xrp(self, seed: str, amount: float, destination: str):
        """Send XRP from the wallet to a destination address"""
        sending_wallet = xrpl.wallet.Wallet.from_seed(seed)
        payment = xrpl.models.transaction.Payment(
            account=sending_wallet.classic_address,
            amount=xrpl.utils.xrp_to_drops(amount),
            destination=destination
        )
        try:
            response = xrpl.transaction.submit_and_wait(payment, self.client, sending_wallet)
        except xrpl.transaction.XRPLReliableSubmissionException as e:
            response = f"Submit failed: {e}"
        return response