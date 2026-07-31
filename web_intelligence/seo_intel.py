from
 typing 
import
 Dict
,
 List
,
 Any


class
 
SEOKptimize
 meta tags"
]
,

            
"Add structured data markup"
,

            
"Create XML sitemap"

        
]

    
    
def
 
generate_meta_tags
(
self
,
 page_info
:
 Dict
[
str
,
 
str
]
)
 
-
>
 
str
:

        
"""Generate SEO meta tags."""

        
return
 
f"""<meta name="description" content="
{
page_info
.
get
(
'description'
,
 
''
)
}
">
<meta name="keywords" content="
{
page_info
.
get
(
'keywords'
,
 
''
)
}
">
<meta property="og:title" content="
{
page_info
.
get
(
'title'
,
 
''
)
}
">
<meta property="og:description" content="
{
page_info
.
get
(
'description'
,
 
''
)
}
">
<meta name="robots" content="index, follow">"""



### web_intelligence/performance_intel.py