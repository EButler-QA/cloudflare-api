# cloudflare-api

This is an API that facilitates the domains management on cloudflare from the command line.

For now, there are 4 possible commands:

create: expects 2 additional arguments, first: new domain name, second: ip

example: cloudflare.py create example.enable.qa 127.0.0.1

delete: expects 1 additional argument, domain to delete

example: cloudflare.py delete example.enable.qa

search-domain: expects 1 additional argument, domain to search for

example: cloudflare.py search-domain example.enable.qa

search-zone: expects 1 additional argument, zone to search for

example: cloudflare.py search-zone example.enable.qa
