from sidt.utils.proxy import Njord

client = Njord().client

print(client.is_protected())

client.disconnect()

print(client.is_protected())

client.connect()

print(client.is_protected())