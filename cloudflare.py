import sys
import json
import requests


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


def print_request(request):
    print("URL: ", request.request.url)
    print("Headers: ")
    print(json.dumps(dict(request.request.headers), sort_keys=False, indent=4))
    print("Body: ")
    if request.request.body is not None:
        print(request.request.body)
    prettify(request.json())


def prettify(response):
    json_formatted_str = json.dumps(response, indent=2)
    print(json_formatted_str)


def search_item(url):
    headers = {'Content-Type': 'application/json'}

    r = requests.get(url,
                     auth=BearerAuth('TVVSMS7bicYwu-PiBa7FH436l4O351gD9scUQ2ui'),
                     headers=headers)

    print_request(r)
    response = r.json()

    record_id = None

    if len(response["result"]) > 0:
        record_id = response["result"][0]["id"]

    return record_id


def search_domain(zone_id, full_domain, record_type="A"):
    print("Search domain: ")
    url = "https://api.cloudflare.com/client/v4/zones/" + \
          zone_id + "/dns_records?match=all&type=" + \
          record_type + "&name=" + full_domain
    return search_item(url)


def search_zone(domain):
    print("Search zone: ")
    url = "https://api.cloudflare.com/client/v4/zones?match=all&type=A&name=" + domain
    return search_item(url)


def create_domain(zone_id, sub_domain, content, record_type="A", ttl=3600, proxied=False):
    print("Create domain: ")
    url = "https://api.cloudflare.com/client/v4/zones/" + zone_id + "/dns_records"
    headers = {'Content-Type': 'application/json'}
    data = {"type": record_type,
            "name": sub_domain,
            "content": content,
            "ttl": ttl,
            "priority": 10,
            "proxied": proxied}

    r = requests.post(url,
                      auth=BearerAuth('TVVSMS7bicYwu-PiBa7FH436l4O351gD9scUQ2ui'),
                      data=json.dumps(data),
                      headers=headers)

    print_request(r)

    return r.json()["success"]


def delete_domain(zone_id, full_domain, record_type="A"):
    print("Delete domain: ")
    record_id = search_domain(zone_id, full_domain, record_type)

    result = False

    if record_id is not None:
        url = "https://api.cloudflare.com/client/v4/zones/" + zone_id + "/dns_records/" + record_id
        headers = {'Content-Type': 'application/json'}

        r = requests.delete(url,
                            auth=BearerAuth('TVVSMS7bicYwu-PiBa7FH436l4O351gD9scUQ2ui'),
                            headers=headers)

        print_request(r)
        response = r.json()

        result = response["success"]

    return result


command = sys.argv[1]

full_domain = sys.argv[2]
full_domain_list = full_domain.split(".")

sub_domain = full_domain_list[0]
domain = full_domain_list[1] + "." + full_domain_list[2]

zone_id = search_zone(domain)

print("Command: {}\nZone ID: {}\nSub-Domain: {}\nDomain: {}".format(command, zone_id, sub_domain, domain))

if command == "create":
    content = sys.argv[3]
    try:
        record_type = sys.argv[4]
        ttl = int(sys.argv[5])
        proxied = sys.argv[6] == "True"
        result = create_domain(zone_id, sub_domain, content, record_type, ttl, proxied)
    except IndexError:
        print("No extra parameters")
        result = create_domain(zone_id, sub_domain, content)
    if result:
        print("Record successfully created")
        sys.exit(0)
    else:
        print("Error while creating the record")
        sys.exit(1)
elif command == "delete":
    try:
        record_type = sys.argv[3]
        result = delete_domain(zone_id, full_domain, record_type)
    except IndexError:
        print("No extra parameters")
        result = delete_domain(zone_id, full_domain)
    if result:
        print("Record successfully deleted")
        sys.exit(0)
    else:
        print("Error while deleting the record")
        sys.exit(1)
elif command == "search-domain":
    result = search_domain(zone_id, full_domain)
    if result is not None:
        print("Domain ID found: {}".format(result))
        sys.exit(0)
    else:
        print("No domain id found for {}".format(full_domain))
        sys.exit(1)
elif command == "search-zone":
    result = search_zone(domain)
    if result is not None:
        print("Zone ID found: {}".format(result))
        sys.exit(0)
    else:
        print("No zone id found for {}".format(full_domain))
        sys.exit(1)
