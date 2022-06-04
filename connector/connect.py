import plaid
from plaid.api import plaid_api
from plaid.model.products import Products
from plaid.model.country_code import CountryCode

configuration = plaid.Configuration(
        host=plaid.Environment.Development,
        api_key={
            'client_id' : '',
            'secret' : '',
        }
)

api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)

bank_name = 'Navy Federal'
products = [Products('transactions')]
country_codes = [CountryCode('US')]

request = plaid_api.InstitutionsSearchRequest(bank_name, products, country_codes)

print(client.institutions_search(request))
