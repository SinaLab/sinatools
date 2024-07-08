from . import synonyms_level2_dict, synonyms_level3_dict

def dfs(graph, start, end, level):
    level = level - 2
    edge = [(start, [])]
    while edge:
        state, path = edge.pop()
        if path and state == end:
            yield path
            continue
        for next_state in graph[state]:               
            if next_state not in path:
               edge.append((next_state, path+[next_state]))
            
            if len(path) > level:               
               break 


def find_cycles(level, synset, used_graph):
    cycles = [] 
    source_with_unique_candidates = {}
    for source in synset:
        source_with_unique_candidates[source] = set()

        for path in dfs(used_graph, source, source, level):  
            cycle = [source]+path
            if len(cycle) <= level : 
               cycles.append(cycle)
            source_with_unique_candidates[source] =  set(source_with_unique_candidates[source].union(set(cycle)))
    return cycles, source_with_unique_candidates   



def get_list_of_unique_synonems(synset,cycles, unique_synonyms, synonems_with_unique_candidates):
    list_of_unique_synonyms = []
    for i in range(0, len(unique_synonyms)):
        synonym = unique_synonyms[i]
        count = 0
        syn_count = 0
        for cycle in cycles:
            if synonym in cycle:
               count = count + 1    

        for v in synonems_with_unique_candidates:
            tmp = list(synonems_with_unique_candidates[v])
            if synonym in tmp :
               syn_count = syn_count + 1
           
           
        list_of_unique_synonyms.append([synonym,count, syn_count])        
    return list_of_unique_synonyms


def find_fuzzy_value_for_candidates(level, list_of_unique_synonyms, number_of_cycles, length_of_synset, synset):
    list_of_synon_with_fuzzy_value = [] 

    if level == 4 : 
       theta1 = 0.5
       theta2 = 0.5
    elif level == 3: 
       theta1 = 0.4
       theta2 = 0.6
    elif level == 2: 
       theta1 = 0.4
       theta2 = 0.6   
    else:
       theta1 = 0
       theta2 = 0
    
    for unique_syn in list_of_unique_synonyms:
        if unique_syn[0] not in synset:    
           equ = ( unique_syn[1] / number_of_cycles ) * theta1 + (unique_syn[2] / length_of_synset ) * theta2     
           list_of_synon_with_fuzzy_value.append([unique_syn[0], equ])
    return list_of_synon_with_fuzzy_value


def extend(synset, level):
   
    used_graph = {}
    if level == 2:
       used_graph = synonyms_level2_dict
    elif level == 3:
       used_graph = synonyms_level3_dict
    else: 
       return "Please choose the correct level"   
    
    cycles = []
    nodes = []
    synonems_with_unique_candidates = {}
    number_of_cycles = 0
    final_synset = []
    
    for syn in synset:
        if syn in list(used_graph.keys()):
          synonems_with_unique_candidates[syn] = set()
          final_synset.append(syn)
          
          cycles_list = used_graph[syn]
          number_of_cycles = number_of_cycles + len(cycles_list)
          for cycle in cycles_list:
             cycles.append(cycle)
             for c in cycle:
                nodes.append(c)
                synonems_with_unique_candidates[syn] = set(synonems_with_unique_candidates[syn].union(set([c])))                   
    
    unique_synonyms = list(set(nodes))
    list_of_unique_synonyms = get_list_of_unique_synonems(final_synset, cycles, unique_synonyms, synonems_with_unique_candidates)
    
    length_of_synset = len(final_synset)
    
    list_of_synon_with_fuzzy_value = find_fuzzy_value_for_candidates(level, list_of_unique_synonyms, number_of_cycles, length_of_synset, final_synset)

    list_of_synon_with_fuzzy_value.sort(key=lambda row: (row[1], row[0]), reverse=True)

    return list_of_synon_with_fuzzy_value