from core_setup import *

p = Parameters()
test.info(p.language)

test.info(f'Found at {p.termbase_path} ')

g_count = 0
g_diffs = 0    # a duplicate entry with at least one difference
g_doubles = 0  # a duplicate entry with no differences
show_only = 0


def is_table_line( x_line, with_columns, x_seperator = '|', x_line_start='| '):
    global g_count 
    r_result = False
    if x_line.count(x_seperator) >= with_columns + 1:
        
        if x_line.find(x_line_start) == 0:
            r_result = True
            g_count += 1

    return r_result


def found_separator_line( x_line, with_columns, x_seperator = '|', x_fill_char = '-' ):
    global g_count 
    r_result = False
    if x_line.count(x_seperator) >= with_columns + 1:
        if x_line.count(x_fill_char) >= int(len(x_line) * 0.7):
            r_result = True
        else:
            pass # test.debug(len(x_line) * 0.7)

    return r_result

last_line = ''
number_of_columns = 9

def strip_spaces_in_line(line):
    line = line.strip()
    line = line.rstrip()
    #line = line.replace(' ', '_')

    return line


class Entry:
    headings=[]

    def __init__(self):
        pass

    def fill(self, data):
        """
        fill data as attributes in class
        """        
        for item_position in range(min(len(data), len(Entry.headings))):
            setattr(self, Entry.headings[item_position], strip_spaces_in_line(data[item_position]))

        return self

    def diff(self, other):
        r_count_equal = 0
        r_count_diff = 0

        for key in Entry.headings:
            if key == 'More': continue

            this = getattr(self, key)
            them = getattr(other, key)

            if this == them or this == '' or them == '':
                r_count_equal += 1
            else:
                r_count_diff += 1
        
        if r_count_diff > 0:
            pass # print(r_count_diff, r_count_equal)

        return r_count_diff, r_count_equal

    def __str__(self):
        output = f'''
---
term:      "{self.Original_Term}"
use:       "{self.Choice_1}"
choices:   ["{self.Choice_2}", "{self.Choice_3}" ]
avoid:     ["{self.Do_Not_Use}"]
reference: {self.Ref}        
state:     {self.State}
date:      "2022-01-05"

---

## Diskussion
{self.Discussion}
'''
        return output\
            .replace(', ""' , '')\
            .replace(', "--" ' , '')\
            .replace('["--", "--" ]', "[]")\
            .replace('["" ]', '[]')\
            .replace('[""]', '[]')\
            .replace('" ]', '"]')\
            .replace("C&C", "compact & very common in daily usage") 


class Termbase:
    def __init__(self):
        self.terms = []
        self.entry = {}

    def add(self, new_entry ):
        global g_diffs
        global g_doubles

        r_is_new = True

        if entry.Original_Term in self.terms:
            r_is_new = False
        else:
            self.terms.append(new_entry.Original_Term)

        if r_is_new:
            self.entry[entry.Original_Term] = new_entry 
        else:
            given_entry = self.entry[entry.Original_Term] 
            #TODO 
            
            count_diff, count_equal = given_entry.diff(new_entry)
            if count_diff > 0:
                g_diffs += 1
                print(f'termbase allready has an entry named {new_entry.Original_Term}')
            else:
                g_doubles += 1
                # print(given_entry.Original_Term)
            if given_entry.Choice_1 != new_entry.Choice_1:
                pass # print(given_entry.Choice_1, new_entry.Choice_1)

        return r_is_new

        
termbase = Termbase()

has_heading = False

with open(p.termbase_path, 'r') as termbase_file:
    for line in termbase_file.readlines():

        if found_separator_line(line, number_of_columns):
            print('process heading ...')
            if len(last_line) > ( number_of_columns * 2):
                raw_headings = last_line.split('|')
                headings = []
                for item in raw_headings:
                    item = strip_spaces_in_line(item)
                    item = item.replace(' ', '_')
                    item = item.replace('-', '_')
                    item = item.replace('.', '')

                    headings.append(item)

                headings = headings[1:-1] 
                has_heading = True


                Entry.headings = headings
                print(f'found {Entry.headings}')
        
        elif is_table_line(line, number_of_columns):
            data = line.split('|')[1:-1]
            entry = Entry().fill(data)
            
            if has_heading:
                new_entry = termbase.add(entry)
            
            if show_only > 0:
                show_only -= 1
                print(e)
        
            
        last_line = line

    print(f'found {g_count} table entries, {g_diffs} and {g_doubles}.')


count = 10
glossary_path = Path('C:/__sync/obs_translation_shared/term_base/de/glossary/')
for entry_key in termbase.entry.keys():
    file_path = glossary_path / f'{entry_key}.de.md'
    print(file_path)

    with open(file_path, 'w') as output_file:
        output_file.write( str(termbase.entry[entry_key]) )
