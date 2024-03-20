# GoDaddy DDNS / DNS Updater
... well, it's kind of a self-explanatory title, isn't it? ;)

This repository contains Python code that uses your GoDaddy API key and secret to automatically create and/or update your A and AAAA records
to point to the current host.
Old records won't be deleted, however.

Comes with `setup.py` and `Dockerfile` to make your life easier ;)

## (Required) environmental variables
<table>
<tr>
<th><h3>Environmental variable</h3></th>
<th><h3>Explanation</h3></th>
</tr>

<tr>
<th>GODADDY_API_KEY</th>
<th>Your GoDaddy API key</th>
</tr>

<tr>
<th>GODADDY_API_SECRET</th>
<th>Your GoDaddy API secret</th>
</tr>

<tr>
<th>DOMAIN</th>
<th>The domain you want to manage. E.g. for <code>a.example.com</code> this would be <code>example.com</code>.
Only one domain can be used at a time.</th>
</tr>

<tr>
<th>SUBDOMAINS</th>
<th>A comma-separated list of subdomains that should be managed by this app.
E.g. for <code>a.example.com</code> and <code>b.example.com</code>, provide <code>a,b</code>.</th>
</tr>

<tr>
<th>TTL</th>
<th>The fixed TTLs for all managed records. Even if the IP addresses for all records are up-to-date, the records will be
updated if the TTLs don't match with this value. Defaults to <code>1200</code> if not provided.</th>
</tr>

<tr>
<th>TIMEOUT</th>
<th>The (min.) timeout in seconds between each update iteration.
Please take into mind that this app. takes into account the 60 requests / min. rate limitation of GoDaddy's API, 
and thus the actual timeout may take longer (in more extreme scenarios). Defaults to <code>300</code> if not provided.</th>
</tr>

<tr>
<th>LOG_LEVEL</th>
<th>The logging level. Defaults to <code>INFO</code> if not provided.</th>
</tr>
</table>