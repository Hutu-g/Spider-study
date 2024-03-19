for page in range(3):
    if page == 0:
        url = "https://www.zbj.com/fw/dmfj/r2/"
        print(url)
    else:
        url = f"https://www.zbj.com/fw/dmfj/r2p{page+1}/?osStr=ad-10,np-0,rf-0,sr-{page * 60 - 7},mb-0"
        print(url)