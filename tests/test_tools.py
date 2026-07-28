import
 pytest

from
 tools
.
file_tool 
import
 FileTool


@pytest
.
mark
.
asyncio


async
 
def
 
test_file_tool_write_read
(
)
:

    
"""Test file writing and reading."""

    config 
=
 
{
"tools"
:
 
{
"file_tool"
:
 
{
"allowed_extensions"
:
 
[
".txt"
]
,
 
"max_file_size_mb"
:
 
10
}
}
}

    tool 
=
 FileTool
(
config
)

    
    test_file 
=
 
"test.txt"

    content 
=
 
"Hello, World!"

    
    success 
=
 
await
 tool
.
write_file
(
test_file
,
 content
)

    
assert
 success
    
    read_content 
=
 
await
 tool
.
read_file
(
test_file
)

    
assert
 read_content 
==
 content
    
    
# Cleanup

    Path
(
test_file
)
.
unlink
(
)



### docs/architecture.md