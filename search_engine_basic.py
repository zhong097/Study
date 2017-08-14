import urllib

Poctuation = ' .,:;"\'!@$'

def get_page(url):
    try:
        content = urllib.urlopen(url).read()
        return content
    except:
        return ''
        

def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1: 
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote


def get_all_links(page):
    links = []
    while True:
        url, endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links


def union(a, b):
    for e in b:
        if e not in a:
            a.append(e)



def split_string(source,splitlist):
    output = []
    mark = True
    for i in source:
        if i in splitlist: 
            mark = True
        else:
            if mark:
                output.append(i)
                mark = False
            else:
                output[-1] = output[-1]+i
    return output
    



def add_to_index(index, keyword, url):
    if keyword in index:
        if url not in index[keyword]:
            index[keyword].append(url)
    else:
        index[keyword] = [url]



def add_page_to_index(index, url, content):
    words = split_string(content, Poctuation)
    for word in words:
        add_to_index(index, word, url)
        

def lookup(index, keyword):
    if keyword in index:
        return index[keyword]
    else:
        return None




def crawl_web(seed): # returns index, graph of inlinks
    tocrawl = [seed]
    crawled = []
    graph = {}  # <url>, [list of pages it links to]
    index = {} 
    while tocrawl: 
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page)
            add_page_to_index(index, page, content)
            outlinks = get_all_links(content)
            graph[page] = outlinks
            union(tocrawl, outlinks)
            crawled.append(page)
    return index, graph




#If want to limit the maximum depth of links
#def crawl_web(seed,max_depth):
#    tocrawl = [seed]
#    crawled = []
#    next_depth = []
#    depth = 0
#    while tocrawl and depth <= max_depth :
#        page = tocrawl.pop()
#        if page not in crawled:
#            union(next_depth, get_all_links(get_page(page)))
#            crawled.append(page)
#        if not tocrawl:
#            tocrawl, next_depth = next_depth, []
#            depth += 1
#    return crawled





def compute_ranks(graph):
    d = 0.8 # damping factor
    numloops = 10
    
    ranks = {}
    npages = len(graph)
    for page in graph:
        ranks[page] = 1.0 / npages
    
    for i in range(0, numloops):
        newranks = {}
        for page in graph:
            newrank = (1 - d) / npages
            for url in graph:
                if page in graph[url]:
                    newrank += d*ranks[url]/len(graph[url])           
            newranks[page] = newrank
        ranks = newranks
    return ranks
    
 
def quicksort(urls,ranks):
    if not urls or len(urls) <= 1:
        return urls
    else:
        pivot = ranks[urls[0]]
        worse = []
        better = []
        for url in urls[1:]:
            if ranks[url] <= pivot:
                worse.append(url)
            else:
                better.append(url)
        return quicksort(better,ranks) + [urls[0]] + quicksort(worse,ranks)
        
        

def ordered_search(index, ranks, keyword):
    urls = lookup(index,keyword)
    return quicksort(urls,ranks)
 
 
    

seed = 'http://www.google.com'
index, graph = crawl_web(seed)
ranks = compute_ranks(graph)



if __name__ == '__main__':
    keyword = raw_input("Type Your Key Word: ")
    result = ordered_search(index, ranks, keyword)
    print result
    


            
            
