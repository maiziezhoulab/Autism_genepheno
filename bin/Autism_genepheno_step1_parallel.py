def get_dirs():
    ASDPTO_dir = './source/ASDPTO.csv'
    UMLS_dir = './source/UMLS.txt'
    allGene_dir = './source/VariCarta_Autism_gene.tsv'
    papers_dir = './XML_Autism_datasets_5years/'
    
    out_dir = './Autism_genepheno_results/'
    
    HPOtreeview_dir = './HPO_treeview.txt'   # From https://raw.githubusercontent.com/obophenotype/human-phenotype-ontology/master/hp.obo'
    return(ASDPTO_dir, UMLS_dir, HPOtreeview_dir, allGene_dir, papers_dir, out_dir)

def handle_HPO_treeview():
    
    ASDPTO_dir, UMLS_dir, HPOtreeview_dir, allGene_dir, papers_dir, out_dir = get_dirs()
    f = open(HPOtreeview_dir, encoding="utf8")
    text = f.read()
    f.close()
    
    HPO = text.split('\n\n[Term]\n')[2:]
    for i in range(len(HPO)):
        HPO[i] = HPO[i].split('\n')
    HP_dic = {}
    for item in HPO:
        HPid = item[0][4:]
        for line in item[1:]:
            if 'name:' in line:
                name = line[6:]
                HP_dic[name] = HPid
            elif 'synonym:' in line:
                b = line.find('"')
                e= line[b+1:].find('"')
                syn = line[b+1:b+e+1]
                HP_dic[syn] = HPid
                
    dic = {}
    for item in HPO:
        HPid = item[0][4:]
        xref = 'NULL'
        is_a_ls = []
        for line in item[1:]:
            if 'name:' in line:
                name = [line[6:]]
            elif 'xref: UMLS:' in line:
                xref = line[11:]
            elif 'is_a:' in line:
                is_a_ls.append(line[6:16])
            elif 'synonym:' in line:
                b = line.find('"')
                e= line[b+1:].find('"')
                name.append(line[b+1:b+e+1])
        name_ = list(set(name))
        name_.sort(key = name.index)
        dic[HPid] = {'name':name_, 'xref':xref, 'is_a':is_a_ls}
        
    upper_dic = {}
    del_hierarchy_ls = ['All']

    for key in dic:

        ls = []
        HP_ls = copy.deepcopy(dic[key]['is_a'])

        if 'HP:0000001' in HP_ls:
            HP_ls.remove('HP:0000001')
        if 'HP:0000118' in HP_ls:
            ls.append(dic[key]['name'][0])

        while HP_ls:
            HP = HP_ls.pop()
            if 'HP:0000118' in dic[HP]['is_a']:
                ls.append(dic[HP]['name'][0])
            for HP_ in dic[HP]['is_a']:
                if HP_ != 'HP:0000001':
                    HP_ls.append(HP_)

        if ls:
            for name in dic[key]['name']:
                upper_dic[name] = list(set(ls))
        else:
            for name in dic[key]['name']:
                del_hierarchy_ls.append(name)
                
    return(upper_dic, HP_dic, del_hierarchy_ls)

def XML_reader(f_path):

    s_list = []
    f_name = open(f_path, encoding="utf8")
    f = f_name.read()
    f_name.close()
    
    #To get the pub date
    h = f.find('<pub-date pub-type="epub">')
    if h == -1:
        date = 'NULL'
    else:
        f_date = f[h:h+80]
        h = f_date.find('<day>')
        e = f_date.find('</day>')
        date = '/' + f_date[h+5:e] + '/'
        h = f_date.find('<month>')
        e = f_date.find('</month>')
        date = f_date[h+7:e] + date
        h = f_date.find('<year>')
        e = f_date.find('</year>')
        date += f_date[h+6:e]
    
    #To get the title
    h = f.find('<article-title>')
    e = f.find('</article-title>')
    title = f[h+15:e]
    title = re.sub('<.*?>', '', title)
    title += ' (Published on ' + date + ')'
    
    ab = ''
    h = f.find('<abstract')
    e = f.find('</abstract>')
    ab = f[h:e]
    
    #To get the body
    h = f.find('<body>')
    e = f.find('</body>')
    
    if h == -1:
        title += ' [Only abstract]'
        
    f = ab + ' ' + f[h:e]
    
    #Replacements for more accurate sentence breaks
    f = f.replace('\n', ' ')
    f = f.replace('Fig. ', 'Fig.')
    f = f.replace('i.e. ', 'i.e.')
    
    #To eliminate reference, table, alternatives
    f = re.sub('<ref.*?/ref>', '', f)    
    f = re.sub('<table.*?/table>', ' ', f)  
    f = re.sub('<alternatives.*?/alternatives>', ' ', f) 
    
    #To eliminate all '<*>'s
    f = re.sub('<.*?>', '', f)
    
    #Sentence breaks using NLTK package
    s_list = sent_tokenize(f)
    
    #To eliminate table/figure names
    for i in range(len(s_list)):
        sp = s_list[i].rfind('   ')
        if sp != -1:
            s_list[i] = s_list[i][sp:]
        s_list[i] = s_list[i].strip()
        
    return(title,s_list)

#The following function is to extract genotype and phenotype in a given sentence.

def gp_extraction(s, g_ls, p_dic):
    
    #s = re.sub('\(.*?\)', '', s)
    s_tokens = re.findall("[A-Za-z0-9\-]+", s)
    s_tokens_origin = copy.deepcopy(s_tokens)
    
    eg_list = []
    for item in s_tokens:
        if item in g_ls:
            eg_list.append(item)
    
    if len(eg_list) == 0:
        return(1,1,1)
    
    ep_list = []
    op_list = []
    
    lemmatizer = WordNetLemmatizer()
    for i in range(len(s_tokens)):
            if not s_tokens[i].isupper():
                s_tokens[i] = lemmatizer.lemmatize(s_tokens[i].lower())
    
    s_tokens_str = str(s_tokens)

    for key in p_dic:
        if p_dic[key] in s_tokens_str:
            ep_list.append(key)
            
            b = 0
            e = 0
            for i in range(4, s_tokens_str.find(p_dic[key])+2):
                if s_tokens_str[i-4:i] == '\', \'':
                    b += 1
            for i in range(4, s_tokens_str.find(p_dic[key])+len(p_dic[key])):
                if s_tokens_str[i-4:i] == '\', \'':
                    e += 1
            op = ''
            for i in range(b, e+1):
                op = op + s_tokens_origin[i] + ' '
            op = op[:-1]
            op_list.append(op)
    
    if len(ep_list) != 0:
        eg_list = sorted(set(eg_list), key=eg_list.index)
        op_list = sorted(set(op_list), key=op_list.index)

        return(eg_list, ep_list, op_list)
    
    return(1,1,1)

def get_phenotype_lists():
    
    ASDPTO_dir, UMLS_dir, HPOtreeview_dir, allGene_dir, papers_dir, out_dir = get_dirs()
    
    #Files reading(ASDPTO.csv).
    ASDPTO_ls = []

    with open(ASDPTO_dir, 'r') as f:
        ASDPTO_file = csv.reader(f)

        mk = 0
        for row in ASDPTO_file:
            if mk == 1:
                ASDPTO_ls.append(row[1])
            mk = 1
            
    # To read phenotype list generated from UMLS
    UMLS = UMLS_dir
    UMLS_ls = []
    source_dic = {}
    cid2c = {}
    c2cid = {}
    sSTT = {}

    f_name = open(UMLS, encoding="utf8")
    f = f_name.read()
    f_name.close()

    f = f.split('\n')
    f = f[:-1]

    all_upper = []

    for line in f:
        cid = line[1:9]
        line = line[12:]
        m0 = line.find('"|')

        concept = line[:m0]
        if concept.isupper():
            all_upper.append(concept)
            continue

        line = line[m0+3:]
        m1 = line.find('"|')
        m2 = line.rfind('|"')
        source = line[:m1]
        STT = line[m2+2:-1]

        if concept in c2cid:
            if cid not in c2cid[concept]:
                c2cid[concept].append(cid)
        else:
            c2cid[concept] = []
            c2cid[concept].append(cid)


        if cid in cid2c:
            cid2c[cid].append(concept)
        else:
            cid2c[cid] = []
            cid2c[cid].append(concept)

        if concept not in UMLS_ls:
            UMLS_ls.append(concept)

        if concept not in source_dic:
            source_dic[concept] = source + ', '
        else:
            if (source + ', ') not in source_dic[concept]:
                source_dic[concept] = source_dic[concept] + source + ', '

        inf = cid+' from '+source+'('+STT+')'
        if concept not in sSTT:
            sSTT[concept] = []
            sSTT[concept].append(inf)
        else:
            if (inf) not in sSTT[concept]:
                sSTT[concept].append(inf)
                
    
    pri = ['HPO(PF)', 'HPO', 'PF','']
    u_c2cid = {}
    c_best_source = {}
    for c in sSTT:
        for s in pri:
            for item in sSTT[c]:
                if s in item:
                    u_c2cid[c] = item[:8]
                    c_best_source[c] = item[14:]
                    break
            else:
                continue
            break  

    #To combine UMLS and ASDPTO

    merged_ls = UMLS_ls
    for concept in ASDPTO_ls:
        if concept not in merged_ls:
            merged_ls.append(concept)
            source_dic[concept] = 'ASDPTO' + ', '
        else:
            source_dic[concept] = source_dic[concept] + 'ASDPTO' + ', '

    merged_ls = list(set(merged_ls))

    '''
    merged_ls = ['UMLS concept 1', 'UMLS concept 2', ..., 'ASDPTO concept 1', ...]
    source_dic = {'Concept 1': 'Source A',
                  'Concept 2': 'Source B, source C, ...',
                   ...}
    c2cid = {'Concept 1': ['CID 1'],
             'Concept 2': ['CID 2', 'CID 3'],
             ...}
    cid2c = {'CID 1': ['Concept 1', 'Concept 2', ...],
             'CID 2': ['Concept 5', 'Concept 6', ...],
             ...}
    '''

    #To delete selected phenotypes and their synonyms
    #del_ls: manually eliminated. del_ls_ASDPTO: high level words of ASDPTO. del_ls_HPO: top 2 level words of HPO

    del_ls = ['Fitting', 'Sharing', 'Sharp', 'Smoking', 'Phenotypic variability', 'Pain', 'Spots', 'Planning', 'Syncope', 'Family history of cancer', 
              'Medical History', 'Social Interest', 'Illness', 'Falls', 'Fit', 'Painful', 'Blood spots', 'Autism Spectrum Disorders', 'Affect', 'Imbalance', 
              'Childhood autism', 'Severe', 'Signs and Symptoms', 'Blocking', 'Autoimmunity', 'Beta-EEG', 'Dependence', 'Imbalance', 'Diagnosis', 'Syncope', 
              'Social Interest', 'Autism', 'Exposures', 'Medications', 'Sporadic', 'High-functioning autism', 'Dissociation', 'Nonverbal', 'Ritual', 
              'Mannerism', 'Compulsion', 'Autistic behavior', 'Shock', 'Mood', 'Vocalizations', 'Behavioral Symptoms', 'Autism Phenotype', 'Eye Contact', 
              'Circling', 'Executive Function', 'Perinatal Exposures', 'Rigidity', 'Somatic mosaicism', 'Cognitive Ability', 'Self-Care', 'Family history', 
              'Withdrawal', 'Working Memory', 'Autism spectrum disorder', 'Clinical disease AND/OR syndrome', 'Syndrome', 'Nervous tension', 
              'Acquired deficiency', 'Symptom', 'Overlying', 'Ache', 'Adult onset', 'Does not worsen', 'IQ', 'Heterogeneity', 'Oxidative stress', 
              'Infection', 'Weakness']

    del_ls_ASDPTO = ['Medical History', 'Comorbidities',  
                    'Complaints and Indications', 'Neurologic Indications', 'Psychologic Indications', 'Diagnosis', 
                    'Primary Diagnosis', 'Exposures', 'Substance Abuse', 'Perinatal History', 'Perinatal Exposures', 'Personal Traits', 'Cognitive Ability', 
                    'Analytic Capability', 'Reasoning', 'Visual Perception', 'Emotional Traits', 'Affect', 'Mood', 'Executive Function', 
                    'Emotional Regulation and Control', 'Control of Emotional Reactions', 'Impulse Control and Regulation', 'Mental Flexibility', 'Planning', 
                    'Working Memory', 'Task Performance', 'Language Ability', 'Development or Regression of Language Skills', 'Expressive Language', 
                    'Expressive Phonology', 'Non-Verbal Communication', 'Receptive Language', 'Motor Skills', 'Stereotyped, Restricted, and Repetitive Behavior', 
                    'Adherence to Rituals and Routines', 'Restricted and Unusual Interests', 
                    'Social Competence', 'Adaptive Life Skills', 'Community Life Skills', 'Engagement in Social Activities', 'Home Life Skills', 
                    'Performance of Household Tasks', 'Self-Care', 'Interpersonal Interactions', 'Interpersonal Awareness', 'Reciprocal Social Interaction', 
                    'Social Interest', 'Initiating and Responding to Social Overtures', 'Interactions with Friends and Family', 'Recognition of Social Norms', 
                    'Awareness of Social Cues', 'Conversational Skills', 'Ability to Converse in Social Settings', 'Ability to Convey Information', 
                    'Understanding Context']

    c2upper, HP_dic, del_ls_HPO = handle_HPO_treeview()

    del_ls.extend(del_ls_ASDPTO)
    del_ls.extend(del_ls_HPO)

    for item in del_ls:

        if item in c2cid:
            for cid in c2cid[item]:
                for c in cid2c[cid]:
                    if c in merged_ls:
                        merged_ls.remove(c) 
        else:
            if item in merged_ls:
                merged_ls.remove(item)

    for key in source_dic:
        source_dic[key] = source_dic[key][:-2]

    #lemmatize the concepts 
    lemmatizer = WordNetLemmatizer()
    lemmatized_dic = {}
    for concept in merged_ls:
        concept_tokens = re.findall("[A-Za-z0-9\-]+", concept)
        for i in range(len(concept_tokens)):
            if not concept_tokens[i].isupper():
                concept_tokens[i] = lemmatizer.lemmatize(concept_tokens[i].lower())
        lemmatized_dic[concept] = str(concept_tokens)[1:-1]

    '''
    lemmatized_dic = {'Concept 1': "Processed string 1",
                      'Concept 2': "Processed string 2", 
                      ...}
    '''

    #Phenotype normalization
    inverted_lem_dic = {}
    ulc_dic = {}
    nc_dic = {}

    for key in lemmatized_dic:
        if lemmatized_dic[key] not in inverted_lem_dic:
            inverted_lem_dic[lemmatized_dic[key]] = []
        inverted_lem_dic[lemmatized_dic[key]].append(key)

    # To build the dictionary for unique lemmatized concepts
    for key in inverted_lem_dic:
        for s in pri:
            for c in sorted(inverted_lem_dic[key]):
                if c in c_best_source:
                    best_source_here = c_best_source[c]
                else:
                    best_source_here = 'ASDPTO'
                if s in best_source_here:
                    ulc_dic[c] = key
                    break
            else:
                continue
            break

    # To build the dictionary for normalized concepts
    for cid in cid2c:
        if cid in cid2c:
            for s in pri:
                for c in sorted(cid2c[cid]):
                    if s in c_best_source[c]:
                        nc_dic[cid] = c
                        break
                else:
                    continue
                break  
            
    return (ulc_dic, u_c2cid, nc_dic, HP_dic, source_dic)

# The following function is to extract gene and phenotype from the given dataset (eg. papers in the folder 'XML_datasets_5year' here).

def para1(f_path, g_ls, ulc_dic, u_c2cid, nc_dic, c2upper, HP_dic, source_dic, out_dir):
    PMCid = 'PMC' + f_path[-11:-4]
    title, s_list = XML_reader(f_path)

    n = 0 
    dic = {}
    dic_ = {}

    for s in s_list:
        eg_list, ep_list, op_list = gp_extraction(s, g_ls, ulc_dic)

        if eg_list != 1:

            his = set()
            np_list = []
            upper_list = []
            for p in ep_list:
                if p in u_c2cid:
                    cid = u_c2cid[p]
                    nc = nc_dic[cid]
                    if nc not in his:
                        if nc in c2upper:
                            upper_list.extend(c2upper[nc])
                        HPid = 'NULL'
                        if nc in HP_dic:
                            HPid = HP_dic[nc]
                        np_list.append([cid, nc, source_dic[nc_dic[cid]], HPid])
                        his.add(nc)
                else:
                    if p not in his:
                        np_list.append(['ASDPTO', p, source_dic[p], 'NULL'])
                        his.add(p)

            upper_list = sorted(set(upper_list), key=upper_list.index)

            ss = 'Sentence' + str(n)

            if ss not in dic_:
                dic_[ss] = {}

            dic_[ss]['Content'] = s
            dic_[ss]['Gene'] = eg_list
            dic_[ss]['Original phenotype'] = op_list
            dic_[ss]['Standardized phenotype'] = np_list
            dic_[ss]['Top-level concepts (HPO only)'] = upper_list

            n += 1
    if len(dic_) != 0:

        dic['PMCid'] = PMCid
        dic['Title'] = title
        dic['Sentences'] = dic_

        doc = open(out_dir + 'Extraced_results/'+ PMCid + '.json', 'w', encoding="utf8")
        print(json.dumps(dic, sort_keys=False, indent=4, separators=(', ', ': '), ensure_ascii=False), file = doc)
        doc.close()

    print('Doing extraction... ; PMC id:', PMCid, '.')
    
def get_results(f_ls):
    
    ASDPTO_dir, UMLS_dir, HPOtreeview_dir, allGene_dir, papers_dir, out_dir = get_dirs()

    #Files reading(export_latest.tsv). To generate genotype list.

    g_ls = []
    csv.register_dialect('tsv',delimiter='\t',quoting=csv.QUOTE_ALL)

    with open(allGene_dir, 'r') as f:
        g_file = csv.reader(f, 'tsv')    
        m0 = 0
        for row in g_file:
            if m0 == 1:
                g_ls.append(row[13])
            m0 = 1

    g_ls = list(set(g_ls))

    # g_ls = ['genotype 1', 'genotype 2', 'genotype 3', ...]

    ulc_dic, u_c2cid, nc_dic, HP_dic, source_dic = get_phenotype_lists()
    
    c2upper, HP_dic, del_ls_HPO = handle_HPO_treeview()

    pool = Pool(20)  
    pool.map(partial(para1, g_ls, ulc_dic, u_c2cid, nc_dic, c2upper, HP_dic, source_dic, out_dir), f_ls)
    pool.close()  
    pool.join() 
    
def para2(f_path, ug_ls, ulc0_dic, u_c2cid, nc_dic, HP_dic, source_dic, out_dir):
    
    lemmatizer = WordNetLemmatizer()
    dic = {}
    g_counts = {}
    p_counts = {}
    PMCid = 'PMC' + f_path[-11:-4]
    title, s_list = XML_reader(f_path)

    dic['PMCid'] = PMCid
    if '[Only abstract]' in title:
        dic['Only abstract?'] = 'Y'
    else:
        dic['Only abstract?'] = 'N'
    dic['Number of Sentences'] = len(s_list)

    for s in s_list:
        s_tokens = re.findall("[A-Za-z0-9\-]+", s)

        eg_ls = []
        for token in s_tokens:
            if token in ug_ls:
                eg_ls.append(token)
        eg_ls = list(set(eg_ls))        
        for g in eg_ls:
            if g in g_counts:
                g_counts[g] += 1
            else:
                g_counts[g] = 1

        for i in range(len(s_tokens)):
                if not s_tokens[i].isupper():
                    s_tokens[i] = lemmatizer.lemmatize(s_tokens[i].lower())

        s_tokens_str = str(s_tokens)

        ep_ls = []

        for p in ulc0_dic:
            if ulc0_dic[p] in s_tokens_str:
                ep_ls.append(p)
        ep_ls = list(set(ep_ls))

        for p in ep_ls:
            if p in u_c2cid:
                cid = u_c2cid[p]
                nc = nc_dic[cid]
                HPid = 'NULL'
                if nc in HP_dic:
                    HPid = HP_dic[nc]
              #  if (cid + ': ' + nc_dic[cid] + '(from ' + source_dic[nc_dic[cid]] + ')' not in up_ls):
              #      print('!!!!!!!!!',cid + ': ' + nc_dic[cid] + '(from ' + source_dic[nc_dic[cid]] + ')')

                if str([cid, nc, source_dic[nc_dic[cid]], HPid]) in p_counts: 
                    p_counts[str([cid, nc, source_dic[nc_dic[cid]], HPid])] += 1
                else:
                    p_counts[str([cid, nc, source_dic[nc_dic[cid]], HPid])] = 1
            else:
                if str(['ASDPTO', p, source_dic[p], 'NULL']) in p_counts:
                    p_counts[str(['ASDPTO', p, source_dic[p], 'NULL'])] += 1
                else:
                 #   if 'ASDPTO: ' + p + '(from ' + source_dic[p] + ')' not in up_ls:
                 #       print('!!!','ASDPTO: ' + p + '(from ' + source_dic[p] + ')')
                    p_counts[str(['ASDPTO', p, source_dic[p], 'NULL'])] = 1

    dic['n_g'] = g_counts
    dic['n_p'] = p_counts

    doc = open(out_dir + 'Sum_for_each_paper/'+PMCid+'.txt', 'w', encoding="utf8")
    print(json.dumps(dic, sort_keys=False, indent=4, separators=(', ', ': '), ensure_ascii=False), file = doc)
    doc.close()

    print('Summarizing each paper... ; PMC id:', PMCid, '.')
        
def get_sum_for_each_paper(f_ls):
    
    ASDPTO_dir, UMLS_dir, HPOtreeview_dir, allGene_dir, papers_dir, out_dir = get_dirs()

    results_ls = []
    path = out_dir + 'Extraced_results/'
    for root, dirs, files in os.walk(path):
        for file in files:
            f = os.path.join(root,file)
            if ('.json' in f) and ('PMC' in f):
                results_ls.append(f)

    ug_ls = []
    up_ls = []

    for f_path in results_ls:
        f_name = open(f_path, encoding="utf8")
        f = f_name.read()
        f_name.close()
        f = ast.literal_eval(f)
        for s in f['Sentences']:
            ug_ls.extend(f['Sentences'][s]['Gene'])
            for item in f['Sentences'][s]['Normolized phenotype']:
                up_ls.append(item[1])

    ug_ls = list(set(ug_ls))
    up_ls = list(set(up_ls))

    ulc_dic, u_c2cid, nc_dic, HP_dic, source_dic = get_phenotype_lists()

    ulc0_dic = {}

    for p in ulc_dic:
        if p in u_c2cid:
            cid = u_c2cid[p]
            np = nc_dic[cid]
        else:
            np = p

        if np in up_ls:
            ulc0_dic[p] = ulc_dic[p]
    
    pool = Pool(20)  
    pool.map(partial(para2, ug_ls, ulc0_dic, u_c2cid, nc_dic, HP_dic, source_dic, out_dir), f_ls)
    pool.close()  
    pool.join() 
        
def get_sum_all():
    
    print('Getting the final summary...')
    
    ASDPTO_dir, UMLS_dir, HPOtreeview_dir, allGene_dir, papers_dir, out_dir = get_dirs()
    f_ls = []
    path = out_dir + 'Sum_for_each_paper/'
    for root, dirs, files in os.walk(path):
        for file in files:
            f = os.path.join(root,file)
            f_ls.append(f)

    num = 0
    ab_num = 0
    N_totle = 0
    u_g_ls = []
    u_p_ls = []
    n_g = {}
    n_p = {}
    for f_path in f_ls:
        f_name = open(f_path, encoding="utf8")
        f = f_name.read()
        f_name.close()
        f = ast.literal_eval(f)
        if f['Only abstract?'] == 'Y':
            ab_num += 1
        N_totle += f['Number of Sentences']
        for g in f['n_g']:
            u_g_ls.append(g)
            if g in n_g:
                n_g[g] += f['n_g'][g]
            else:
                n_g[g] = f['n_g'][g]
        for p in f['n_p']:
            u_p_ls.append(p)
            if p in n_p:
                n_p[p] += f['n_p'][p]
            else:
                n_p[p] = f['n_p'][p]
        num += 1
        print(num, f_path)
    u_g_ls = list(set(u_g_ls))
    u_p_ls = list(set(u_p_ls))

    results_ls = []
    path = out_dir + 'Extraced_results/'
    for root, dirs, files in os.walk(path):
        for file in files:
            f = os.path.join(root,file)
            if ('.json' in f) and ('PMC' in f):
                results_ls.append(f)

    est_num = 0
    for f_path in results_ls:
        f_name = open(f_path, encoding="utf8")
        f = f_name.read()
        f_name.close()
        f = ast.literal_eval(f)
        est_num += len(f['Sentences'])

    sum_all_dir = out_dir + 'Sum_all/'
    doc = open(sum_all_dir + 'In_Summary.txt', 'w')
    print('Number of paper processed:', len(f_ls), file = doc)
    print(file = doc)
    print('Number of the articles have only abstract:', ab_num, file = doc)
    print(file = doc)
    print('Number of paper get at least one sentence:', len(results_ls), file = doc)
    print(file = doc)
    print('Sentences extracted:', est_num, file = doc)
    print(file = doc)
    print('N_tot = ', N_totle, file = doc)
    print(file = doc)
    #print('Phenotype source distribution:', counts, file = doc)
    #print(file = doc)
    print('Unique gene list from all papers:', u_g_ls, file = doc)
    print(file = doc)
    print('Unique normalized phenotype list from all papers:', u_p_ls, file = doc)
    print(file = doc)
    #print('Unique phenotype source distribution:', u_counts, file = doc)
    #print(file = doc)
    doc.close()

    doc = open(sum_all_dir + 'n_g.txt', 'w')
    print(n_g, file = doc)
    doc.close()

    doc = open(sum_all_dir + 'n_p.txt', 'w')
    print(n_p, file = doc)
    doc.close()
    
#To start/continue the extraction
def find_breakpoint():
    
    ASDPTO_dir, UMLS_dir, HPOtreeview_dir, allGene_dir, papers_dir, out_dir = get_dirs()

    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    if not os.path.exists(out_dir + 'Extraced_results'):
        os.mkdir(out_dir + 'Extraced_results')
    if not os.path.exists(out_dir + 'Sum_for_each_paper'):
        os.mkdir(out_dir + 'Sum_for_each_paper')
    if not os.path.exists(out_dir + 'Sum_all'):
        os.mkdir(out_dir + 'Sum_all')
    
    f_ls = []
    path = papers_dir
    for root, dirs, files in os.walk(path):
        for file in files:
            f = os.path.join(root,file)
            if '.xml' in f:
                f_ls.append(f)

    sum_ls = []
    path = out_dir + 'Sum_for_each_paper/'
    for root, dirs, files in os.walk(path):
        for file in files:
            f = os.path.join(root,file)
            if ('.txt' in f) and ('PMC' in f):
                sum_ls.append(f)
        
    results_ls = []
    path = out_dir + 'Extraced_results/'
    for root, dirs, files in os.walk(path):
        for file in files:
            f = os.path.join(root,file)
            if ('.json' in f) and ('PMC' in f):
                results_ls.append(f)
                
    if len(results_ls) == 0:
        get_results(f_ls)
        get_sum_for_each_paper(f_ls)
        get_sum_all()
    elif len(sum_ls) == 0: 
        x = 0
        for item in results_ls:
            loc = item.find('PMC') + 3
            f = papers_dir + item[loc:-4] + 'xml'
            x = max(x, f_ls.index(f))
        get_results(f_ls[x:])
        get_sum_for_each_paper(f_ls)
        get_sum_all()
    else:
        x = 0
        for item in sum_ls:
            loc = item.find('PMC') + 3
            f = papers_dir + item[loc:-4] + 'xml'
            x = max(x, f_ls.index(f))
        get_sum_for_each_paper(f_ls[x:])
        get_sum_all()
        
# import nltk
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')
from nltk.tokenize import sent_tokenize
from nltk.stem import WordNetLemmatizer
from multiprocessing import Pool
from functools import partial
import copy
import re
import ast
import csv
import json
import os

find_breakpoint()