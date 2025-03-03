import pandas as pd
import numpy as np
import glob

NOTHINGNESS = [
    '            [\"name\"] = \"Nothingness\",\n',
    '            [\"icon\"] = \"Art/2DArt/SkillIcons/passives/MasteryBlank.png\",\n',
    '            [\"stats\"] = {},\n']

NOTHINGNESS_ASCENDANCY = [
    '            [\"name\"] = \"Nothingness\",\n',
    '            [\"icon\"] = \"Art/2DArt/SkillIcons/passives/MasteryBlank.png\",\n',
    '            [\"ascendancyName\"] = \"None\",\n',
    '            [\"stats\"] = {},\n']

def load_tree(fname='./data/tree.lua'):
    return open(fname,'r').readlines()

def save_tree(tree, basedir='./data/', fname='tree_edit.lua'):
    with open(basedir+fname,'w') as f:
        for line in tree:
            f.write(line)

def replace_all_nodes_wrapper():
    original_tree = load_tree()
    modified_tree = load_tree()
    replace_all_nodes(modified_tree, original_tree)

def replace_all_nodes(modified_tree, original_tree, basedir='./data/'):
    all_jsons = glob.glob(basedir+'*.json')
    if len(all_jsons) < 1:
        print('ERROR: no JSON files found in data directory...')
    all_node_data = pd.concat([pd.read_json(json_file, typ='series') for json_file in all_jsons])
    node_df = pd.DataFrame(all_node_data).reset_index().rename(columns = {'index':'original', 0:'new'})
    node_df = node_df.drop_duplicates()
    nothingness_dupes = node_df[node_df['original'].duplicated(keep=False)]
    node_df = node_df.drop(nothingness_dupes[nothingness_dupes['new']==-1].index)

    if any(node_df['original'].duplicated()):
        print('WARNING: mismatched duplicate nodes found:')
        for node_id in np.where(node_df['original'].duplicated())[0]:
            print('mismatch original node: '+str(node_df.iloc[node_id]['original'])) #+', new: '+str(node_df.iloc[node_id]['new']))

    for line in range(len(node_df)):
        replace_node(modified_tree, original_tree,
                int(node_df.iloc[line]['original']), int(node_df.iloc[line]['new']))
    save_tree(modified_tree)

def replace_node(modified_tree, original_tree, node_id, replace_id):
    if type(node_id) == str:
        node_found, node_id = get_node_id_by_name(original_tree, node_id)
        if not(node_found):
            print('original node string not found, returning original_tree')
            return modified_tree
    if type(replace_id) == str:
        replace_found, replace_id = get_node_id_by_name(original_tree, replace_id)
        if not(replace_found):
            print('replacement node string not found, returning original_tree')
            return modified_tree
    node_found, node_start, node_end = get_node_by_id(modified_tree, node_id)
    if replace_id > 0:
        replace_found, replace_start, replace_end = get_node_by_id(original_tree, replace_id)
    else:
        replace_found = True
    is_ascendancy = False
    if node_found and replace_found:
        for line_idx in range(node_end-node_start):
            if 'ascendancyName' in modified_tree[node_start]:
                ascendancy_line = modified_tree[node_start]
                is_ascendancy = True
            modified_tree.pop(node_start)
        if replace_id > 0:
            replace_lines = original_tree[replace_start:replace_end]
        elif is_ascendancy:
            replace_lines = NOTHINGNESS_ASCENDANCY
            replace_start = 0
            replace_end = 4
        else:
            replace_lines = NOTHINGNESS
            replace_start = 0
            replace_end = 3
        for replace_idx, line_idx in enumerate(range(node_start, node_start+replace_end-replace_start)):
            if 'ascendancyName' in replace_lines[replace_idx]:
                try:
                    modified_tree.insert(line_idx, ascendancy_line)
                except:
                    print('error: node '+str(node_id)+'; replace: '+str(replace_id))
            else:
                modified_tree.insert(line_idx, replace_lines[replace_idx])
    else:
        print('node '+str(node_id)+' or replacement '+str(replace_id)+' not found, returning original tree')
    return modified_tree

def get_node_by_id(tree, node_id):
    start_offset = 10553 #10261
    end_offset = 72688 #66842
    subtree = tree[start_offset:end_offset]
    node_str = '['+str(node_id)+']'
    node_start_found = False
    for line_idx, line in enumerate(subtree):
        if node_str in line:
            node_start_idx = line_idx+2
            node_start_found = True
            break
    if node_start_found:
        node_end_found = False
        for line_idx, line in enumerate(subtree[node_start_idx:]):
            if '[\"group\"]' in line:
                node_end_idx = node_start_idx+line_idx
                node_end_found = True
                break
    if node_start_found and node_end_found:
        return True, node_start_idx+start_offset, node_end_idx+start_offset
    else:
        return False, -1, -1

def get_node_id_by_name(tree, node_name):
    node_id_found = False
    node_id = -1
    for line_idx, line in enumerate(tree):
        if node_name in line:
            node_start_idx = line_idx-2
            node_id = tree[node_start_idx].rsplit('[')[1].rsplit(']')[0]
            node_id_found = True
            break
    return node_id_found, node_id
