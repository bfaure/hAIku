from urllib.request import urlopen

def flush_buffer(buf,f):
	for b in buf:
		f.write("%s\n"%b)
	return []

base_url='http://haiku.somebullshit.net/'
dest=open('data.tsv','w')
index=1

buffer_size=1000
haiku_buffer=[] # to be flushed to file
total_haikus=0

while True:
	try:
		url=base_url+"%d.html"%index
		html=urlopen(url).read().decode('utf-8')
		items=html.split("<article class=\"card\">")[1:]
		for item in items:
			text=item.split("<p>")[1].split("</p>")[0].replace("<br>","").replace("&nbsp;","").replace("  "," ").strip("\n").replace("\n","<br>")
			haiku_buffer.append(text)
			total_haikus+=1
		print("\rTotal haikus downloaded: %d"%total_haikus,end="\r")
		if len(haiku_buffer)>buffer_size: haiku_buffer=flush_buffer(haiku_buffer,dest)
	except Exception as e:
		print ("Caught exception: ",e)
		print ("Flushing haiku buffer...")
		flush_buffer(haiku_buffer,dest)
		print ("Done.")
	index+=1

	if index>=1747: break

flush_buffer(haiku_buffer,dest)
print("\n\nDone.")






