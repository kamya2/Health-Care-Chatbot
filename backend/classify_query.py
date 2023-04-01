import os
import ahocorasick

class ClassifyQuery:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        self.disease_path = os.path.join(cur_dir, 'dict/disease.txt')
        self.department_path = os.path.join(cur_dir, 'dict/department.txt')
        self.symptom_path = os.path.join(cur_dir, 'dict/symptoms.txt')

        self.disease_wds = [i.strip() for i in open(
            self.disease_path, 'r', encoding='gbk') if i.strip()]
        self.department_wds = [i.strip() for i in open(
            self.department_path, 'r', encoding='gbk') if i.strip()]
        self.symptom_wds = [i.strip() for i in open(
            self.symptom_path, 'r', encoding='utf-8') if i.strip()]
        self.region_words = set(self.department_wds +
                                self.disease_wds + self.symptom_wds)

        self.region_tree = self.create_actree(list(self.region_words))
        self.wdtype_dict = self.construct_dict()
        self.symptom_qwds = ['symptom', 'characterization', 'phenomenon']
        self.cause_qwds = ['reason', 'cause']
        self.accompany_qwds = ['complication', 'concurrent', 'occur', 'happen together',
                               'occur together', 'appear together', 'together', 'accompany', 'follow', 'coexist']
        self.prevent_qwds = ['prevention', 'prevent', 'resist', 'guard', 'against', 'escape', 'avoid',
                             'how can I not',
                             'how not to', 'why not', 'how to prevent']
        self.lasttime_qwds = ['cycle', 'time', 'day', 'year', 'hour', 'days', 'years', 'hours', 'how long',
                              'how much time', 'a few days', 'how many years', 'how many days', 'how many hours', 'a few hours', 'a few years']
        self.cureway_qwds = ['treat', 'heal', 'cure', 'how to treat',
                             'how to heal', 'how to cure', 'treatment', 'therapy']
        self.cureprob_qwds = ['how big is the hope of cure', 'hope',
                              'probability', 'possibility', 'percentage', 'proportion']
        self.easyget_qwds = ['susceptible population', 'susceptible', 'crowd',
                             'easy to infect', 'who', 'which people', 'infection', 'infect']
        self.belong_qwds = ['what belongs to', 'belong',
                            'belongs', 'section', 'what section', 'department']
        self.cure_qwds = ['what to treat', 'indication',
                          'what is the use', 'benefit', 'usefulness']

    def classify_que_category(self, question):
        data = {}
        question2 = question.lower()
        medical_dict = self.find_health_related_terms(question2)
        if not medical_dict:
            return {}
        data['args'] = medical_dict
        types = []
        for type_ in medical_dict.values():
            types += type_
        question_type = 'others'
        question_types = []

        if self.find_wds(self.symptom_qwds, question2) and ('disease' in types):
            question_type = 'disease_symptom'
            question_types.append(question_type)

        if self.find_wds(self.symptom_qwds, question2) and ('symptom' in types):
            question_type = 'symptom_disease'
            question_types.append(question_type)

        if self.find_wds(self.cause_qwds, question2) and ('disease' in types):
            question_type = 'disease_cause'
            question_types.append(question_type)

        if self.find_wds(self.accompany_qwds, question2) and ('disease' in types):
            question_type = 'disease_accompany'
            question_types.append(question_type)

        if self.find_wds(self.prevent_qwds, question2) and 'disease' in types:
            question_type = 'disease_prevent'
            question_types.append(question_type)

        if self.find_wds(self.lasttime_qwds, question2) and 'disease' in types:
            question_type = 'disease_lasttime'
            question_types.append(question_type)

        if self.find_wds(self.cureway_qwds, question2) and 'disease' in types:
            question_type = 'disease_cureway'
            question_types.append(question_type)

        if self.find_wds(self.cureprob_qwds, question2) and 'disease' in types:
            question_type = 'disease_cureprob'
            question_types.append(question_type)

        if self.find_wds(self.easyget_qwds, question2) and 'disease' in types:
            question_type = 'disease_easyget'
            question_types.append(question_type)

        if question_types == [] and 'disease' in types:
            question_types = ['disease_desc']

        if question_types == [] and 'symptom' in types:
            question_types = ['symptom_disease']

        data['question_types'] = question_types

        return data

    def construct_dict(self):
        wd_dict = dict()
        for wd in self.region_words:
            wd_dict[wd] = []
            if wd in self.disease_wds:
                wd_dict[wd].append('disease')
            if wd in self.department_wds:
                wd_dict[wd].append('department')
            if wd in self.symptom_wds:
                wd_dict[wd].append('symptom')
        return wd_dict

    def create_actree(self, wordlist):
        actree = ahocorasick.Automaton()
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree

    def find_health_related_terms(self, question):
        region_wds = []
        for i in self.region_tree.iter(question):
            wd = i[1][1]
            region_wds.append(wd)

        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)
        final_wds = [i for i in region_wds if i not in stop_wds]
        final_dict = {i: self.wdtype_dict.get(i) for i in final_wds}

        return final_dict

    def find_wds(self, wds, sent):
        for wd in wds:
            if wd in sent:
                return True
        return False


if __name__ == '__main__':
    classifier = ClassifyQuery()
    while True:
        query = input('Enter query:')
        data = classifier.classify_que_category(query)
