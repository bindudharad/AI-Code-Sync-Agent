"""
Diff engine for intelligent file comparison and merging.
"""


import
 difflib

from
 pathlib 
import
 Path

from
 typing 
import
 Dict
,
 List
,
 Any
,
 Optional
,
 Tuple



class
 
DiffEngine
:

    
def
 
__init__
(
self
,
 config
:
 Dict
[
str
,
 Any
]
)
:

        self
.
config 
=
 config
    
    
def
 
compare_files
(
self
,
 old_file
:
 Path
,
 new_file
:
 Path
)
 
-
>
 Dict
[
str
,
 Any
]
:

        
"""Compare two files and return differences."""

        
if
 
not
 old_file
.
exists
(
)
:

            
return
 
{

                
"status"
:
 
"new_file"
,

                
"diff"
:
 
[
]
,

                
"stats"
:
 
{
"added"
:
 
0
,
 
"removed"
:
 
0
,
 
"modified"
:
 
0
}

            
}

        
        old_content 
=
 old_file
.
read_text
(
)
.
splitlines
(
)

        new_content 
=
 new_file
.
read_text
(
)
.
splitlines
(
)

        
        
return
 self
.
compare_content
(
old_content
,
 new_content
,
 old_file
.
name
)

    
    
def
 
compare_content
(

        self
,

        old_content
:
 List
[
str
]
,

        new_content
:
 List
[
str
]
,

        filename
:
 
str
 
=
 
"file"

    
)
 
-
>
 Dict
[
str
,
 Any
]
:

        
"""Compare two content lists."""

        diff 
=
 
list
(
difflib
.
unified_diff
(

            old_content
,

            new_content
,

            fromfile
=
f"
{
filename
}
.old"
,

            tofile
=
f"
{
filename
}
.new"
,

            lineterm
=
""

        
)
)

        
        
# Calculate stats

        added 
=
 
sum
(
1
 
for
 line 
in
 diff 
if
 line
.
startswith
(
"+"
)
 
and
 
not
 line
.
startswith
(
"+++"
)
)

        removed 
=
 
sum
(
1
 
for
 line 
in
 diff 
if
 line
.
startswith
(
"-"
)
 
and
 
not
 line
.
startswith
(
"---"
)
)

        
        
return
 
{

            
"status"
:
 
"modified"
 
if
 diff 
else
 
"unchanged"
,

            
"diff"
:
 diff
,

            
"stats"
:
 
{

                
"added"
:
 added
,

                
"removed"
:
 removed
,

                
"modified"
:
 
max
(
added
,
 removed
)

            
}

        
}

    
    
def
 
apply_diff
(
self
,
 original_file
:
 Path
,
 diff
:
 List
[
str
]
)
 
-
>
 
bool
:

        
"""Apply a diff to a file."""

        
if
 
not
 original_file
.
exists
(
)
:

            
return
 
False

        
        original_content 
=
 original_file
.
read_text
(
)
.
splitlines
(
)

        
        
# Parse diff

        new_content 
=
 self
.
_apply_diff_to_content
(
original_content
,
 diff
)

        
        
if
 new_content 
is
 
None
:

            
return
 
False

        
        
# Write back

        original_file
.
write_text
(
"\n"
.
join
(
new_content
)
)

        
return
 
True

    
    
def
 
_apply_diff_to_content
(

        self
,

        original
:
 List
[
str
]
,

        diff
:
 List
[
str
]

    
)
 
-
>
 Optional
[
List
[
str
]
]
:

        
"""Apply diff to content."""

        
try
:

            
# Simple line-based application (doesn't handle all cases)

            result 
=
 original
.
copy
(
)

            line_num 
=
 
0

            
            
for
 diff_line 
in
 diff
:

                
if
 diff_line
.
startswith
(
"@@"
)
:

                    
# Parse line numbers

                    parts 
=
 diff_line
.
split
(
" "
)

                    new_range 
=
 parts
[
1
]

                    start_line 
=
 
int
(
new_range
.
split
(
","
)
[
0
]
[
1
:
]
)
 
-
 
1

                    line_num 
=
 start_line
                
                
elif
 diff_line
.
startswith
(
"+"
)
:

                    
# Add line

                    result
.
insert
(
line_num
,
 diff_line
[
1
:
]
)

                    line_num 
+=
 
1

                
                
elif
 diff_line
.
startswith
(
"-"
)
:

                    
# Remove line

                    
if
 line_num 
<
 
len
(
result
)
:

                        
del
 result
[
line_num
]

            
            
return
 result
        
        
except
 Exception
:

            
return
 
None

    
    
def
 
merge_files
(

        self
,

        base_file
:
 Path
,

        our_file
:
 Path
,

        their_file
:
 Path
    
)
 
-
>
 Dict
[
str
,
 Any
]
:

        
"""Three-way merge of files."""

        
if
 
not
 base_file
.
exists
(
)
:

            
return
 
{

                
"success"
:
 
False
,

                
"conflicts"
:
 
[
]
,

                
"merged_content"
:
 
None

            
}

        
        base_content 
=
 base_file
.
read_text
(
)
.
splitlines
(
)

        our_content 
=
 our_file
.
read_text
(
)
.
splitlines
(
)

        their_content 
=
 their_file
.
read_text
(
)
.
splitlines
(
)

        
        
return
 self
.
merge_content
(
base_content
,
 our_content
,
 their_content
)

    
    
def
 
merge_content
(

        self
,

        base
:
 List
[
str
]
,

        ours
:
 List
[
str
]
,

        theirs
:
 List
[
str
]

    
)
 
-
>
 Dict
[
str
,
 Any
]
:

        
"""Three-way merge of content."""

        merger 
=
 difflib
.
Differ
(
)

        
        
# Get differences

        our_diff 
=
 
list
(
merger
.
compare
(
base
,
 ours
)
)

        their_diff 
=
 
list
(
merger
.
compare
(
base
,
 theirs
)
)

        
        
# Simple merge strategy

        merged 
=
 base
.
copy
(
)

        conflicts 
=
 
[
]

        
        
for
 i
,
 
(
our_line
,
 their_line
)
 
in
 
enumerate
(
zip
(
our_diff
,
 their_diff
)
)
:

            
if
 our_line
.
startswith
(
"  "
)
 
and
 their_line
.
startswith
(
"  "
)
:

                
# No changes

                
continue

            
            
elif
 our_line
.
startswith
(
"+ "
)
 
and
 their_line
.
startswith
(
"+ "
)
:

                
# Both added (same line)

                
if
 our_line 
==
 their_line
:

                    merged
.
append
(
our_line
[
2
:
]
)

                
else
:

                    
# Conflict

                    conflicts
.
append
(
{

                        
"line"
:
 i
,

                        
"ours"
:
 our_line
[
2
:
]
,

                        
"theirs"
:
 their_line
[
2
:
]
,

                        
"base"
:
 base
[
i
]
 
if
 i 
<
 
len
(
base
)
 
else
 
""

                    
}
)

            
            
elif
 our_line
.
startswith
(
"+ "
)
:

                
# Only we added

                merged
.
append
(
our_line
[
2
:
]
)

            
            
elif
 their_line
.
startswith
(
"+ "
)
:

                
# Only they added

                merged
.
append
(
their_line
[
2
:
]
)

            
            
elif
 our_line
.
startswith
(
"- "
)
 
and
 their_line
.
startswith
(
"- "
)
:

                
# Both removed

                
if
 i 
<
 
len
(
merged
)
:

                    
del
 merged
[
i
]

        
        
return
 
{

            
"success"
:
 
len
(
conflicts
)
 
==
 
0
,

            
"conflicts"
:
 conflicts
,

            
"merged_content"
:
 merged 
if
 
len
(
conflicts
)
 
==
 
0
 
else
 
None

        
}

    
    
def
 
generate_merge_conflict_markers
(

        self
,

        base
:
 List
[
str
]
,

        ours
:
 List
[
str
]
,

        theirs
:
 List
[
str
]

    
)
 
-
>
 List
[
str
]
:

        
"""Generate merge conflict markers."""

        result 
=
 
[
]

        in_conflict 
=
 
False

        
        
for
 i 
in
 
range
(
max
(
len
(
base
)
,
 
len
(
ours
)
,
 
len
(
theirs
)
)
)
:

            base_line 
=
 base
[
i
]
 
if
 i 
<
 
len
(
base
)
 
else
 
None

            our_line 
=
 ours
[
i
]
 
if
 i 
<
 
len
(
ours
)
 
else
 
None

            their_line 
=
 theirs
[
i
]
 
if
 i 
<
 
len
(
theirs
)
 
else
 
None

            
            
if
 our_line 
==
 their_line
:

                
# No conflict

                
if
 in_conflict
:

                    result
.
append
(
">>>>>>> theirs"
)

                    in_conflict 
=
 
False

                result
.
append
(
our_line 
or
 
""
)

            
            
elif
 base_line 
==
 our_line 
and
 base_line 
!=
 their_line
:

                
# Their change

                
if
 
not
 in_conflict
:

                    result
.
append
(
"<<<<<<< ours"
)

                    in_conflict 
=
 
True

                result
.
append
(
their_line 
or
 
""
)

            
            
elif
 base_line 
==
 their_line 
and
 base_line 
!=
 our_line
:

                
# Our change

                
if
 
not
 in_conflict
:

                    result
.
append
(
"<<<<<<< ours"
)

                    in_conflict 
=
 
True

                result
.
append
(
our_line 
or
 
""
)

            
            
else
:

                
# Both changed

                
if
 
not
 in_conflict
:

                    result
.
append
(
"<<<<<<< ours"
)

                    in_conflict 
=
 
True

                result
.
append
(
our_line 
or
 
""
)

                result
.
append
(
"======="
)

                result
.
append
(
their_line 
or
 
""
)

        
        
if
 in_conflict
:

            result
.
append
(
">>>>>>> theirs"
)

        
        
return
 result
    
    
def
 
intelligent_diff
(
self
,
 old
:
 
str
,
 new
:
 
str
)
 
-
>
 Dict
[
str
,
 Any
]
:

        
"""Generate intelligent diff with context."""

        old_lines 
=
 old
.
splitlines
(
)

        new_lines 
=
 new
.
splitlines
(
)

        
        
# Find changes

        diff 
=
 difflib
.
SequenceMatcher
(
None
,
 old_lines
,
 new_lines
)

        
        changes 
=
 
[
]

        
        
for
 tag
,
 i1
,
 i2
,
 j1
,
 j2 
in
 diff
.
get_opcodes
(
)
:

            
if
 tag 
==
 
"replace"
:

                changes
.
append
(
{

                    
"type"
:
 
"modified"
,

                    
"old_lines"
:
 old_lines
[
i1
:
i2
]
,

                    
"new_lines"
:
 new_lines
[
j1
:
j2
]
,

                    
"old_start"
:
 i1
,

                    
"new_start"
:
 j1
                
}
)

            
elif
 tag 
==
 
"delete"
:

                changes
.
append
(
{

                    
"type"
:
 
"removed"
,

                    
"lines"
:
 old_lines
[
i1
:
i2
]
,

                    
"start"
:
 i1
                
}
)

            
elif
 tag 
==
 
"insert"
:

                changes
.
append
(
{

                    
"type"
:
 
"added"
,

                    
"lines"
:
 new_lines
[
j1
:
j2
]
,

                    
"start"
:
 j1
                
}
)

        
        
return
 
{

            
"changes"
:
 changes
,

            
"total_changes"
:
 
len
(
changes
)
,

            
"old_line_count"
:
 
len
(
old_lines
)
,

            
"new_line_count"
:
 
len
(
new_lines
)

        
}



### interface/cli.py