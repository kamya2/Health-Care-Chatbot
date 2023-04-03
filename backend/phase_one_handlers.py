from py2neo import Graph

class FindQueryResultPhaseOne:
    def __init__(self):
        self.g = Graph("bolt://localhost:7687", auth=("neo4j", "12345678"))
        self.num_limit = 20

    def phase_one_searcher(self, cypher_querys):
        final_answers = []
        for cypher_query_ in cypher_querys:
            question_type = cypher_query_['question_type']
            queries = cypher_query_['cypher_query']
            answers = []
            for query in queries:
                ress = self.g.run(query).data()
                answers += ress
            final_answer = self.generate_formatted_response(
                question_type, answers)
            if final_answer:
                final_answers.append(final_answer)
        return final_answers

    def generate_formatted_response(self, question_type, answers):
        final_answer = []
        if not answers:
            return ''
        if question_type == 'disease_symptom':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = 'The symptoms of {0} include: {1}'.format(
                subject, ','.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'symptom_disease':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = 'You entered symptoms as: {0}. You may be infected with: {1}'.format(
                subject, ','.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_cause':
            desc = [i['m.cause'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = 'The possible causes of {0} are: {1}'.format(
                subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_prevent':
            desc = [i['m.prevent'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = 'Precautions for {0} include: {1}'.format(
                subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_lasttime':
            desc = [i['m.cure_lasttime'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = 'The period in which {0} treatment may last is: {1}'.format(
                subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_cureway':
            desc = [';'.join(i['m.cure_way']) for i in answers]
            subject = answers[0]['m.name']
            final_answer = 'For {0}, you can try the following treatments: {1}'.format(
                subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_desc':
            desc = [i['m.desc'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}, familiar with: {1}'.format(
                subject,  '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_acompany':
            desc1 = [i['n.name'] for i in answers]
            desc2 = [i['m.name'] for i in answers]
            subject = answers[0]['m.name']
            desc = [i for i in desc1 + desc2 if i != subject]
            final_answer = 'The symptoms of {0} include: {1}'.format(
                subject, '；'.join(list(set(desc))[:self.num_limit]))
        return final_answer

if __name__ == '__main__':
    phase_one_find_answers = FindQueryResultPhaseOne()
