class QueryGenerator:

    def map_entities(self, args):
        entity_dict = {}
        for arg, types in args.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] = [arg]
                else:
                    entity_dict[type].append(arg)

        return entity_dict

    def generate_query(self, res_classify):
        args = res_classify['args']
        entity_dict = self.map_entities(args)
        question_types = res_classify['question_types']
        cypher_querys = []
        for question_type in question_types:
            cypher_query_ = {}
            cypher_query_['question_type'] = question_type
            cypher_query = []
            if question_type == 'disease_symptom':
                cypher_query = self.generate_cypher(
                    question_type, entity_dict.get('disease'))

            elif question_type == 'symptom_disease':
                cypher_query = self.generate_cypher(
                    question_type, entity_dict.get('symptom'))

            elif question_type == 'disease_cause':
                cypher_query = self.generate_cypher(
                    question_type, entity_dict.get('disease'))

            elif question_type == 'disease_acompany':
                cypher_query = self.generate_cypher(
                    question_type, entity_dict.get('disease'))

            elif question_type == 'disease_prevent':
                cypher_query = self.generate_cypher(
                    question_type, entity_dict.get('disease'))

            elif question_type == 'disease_lasttime':
                cypher_query = self.generate_cypher(
                    question_type, entity_dict.get('disease'))

            elif question_type == 'disease_cureway':
                cypher_query = self.generate_cypher(
                    question_type, entity_dict.get('disease'))

            elif question_type == 'disease_cureprob':
                cypher_query = self.generate_cypher(
                    question_type, entity_dict.get('disease'))

            elif question_type == 'disease_easyget':
                cypher_query = self.generate_cypher(
                    question_type, entity_dict.get('disease'))

            elif question_type == 'disease_desc':
                cypher_query = self.generate_cypher(
                    question_type, entity_dict.get('disease'))

            if cypher_query:
                cypher_query_['cypher_query'] = cypher_query

                cypher_querys.append(cypher_query_)

        return cypher_querys

    def generate_cypher(self, question_type, entities):
        if not entities:
            return []

        cypher_query = []

        if question_type == 'disease_cause':
            cypher_query = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.cause".format(
                i) for i in entities]

        elif question_type == 'disease_prevent':
            cypher_query = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.prevent".format(
                i) for i in entities]

        elif question_type == 'disease_lasttime':
            cypher_query = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.cure_lasttime".format(
                i) for i in entities]

        elif question_type == 'disease_cureprob':
            cypher_query = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.cured_prob".format(
                i) for i in entities]

        elif question_type == 'disease_cureway':
            cypher_query = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.cure_way".format(
                i) for i in entities]

        elif question_type == 'disease_easyget':
            cypher_query = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.easy_get".format(
                i) for i in entities]

        elif question_type == 'disease_desc':
            cypher_query = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.desc".format(
                i) for i in entities]

        elif question_type == 'disease_symptom':
            cypher_query = [
                "MATCH (m:Disease)-[r:has_symptom]->(n:Symptom) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        elif question_type == 'symptom_disease':
            cypher_query = [
                "MATCH (m:Disease)-[r:has_symptom]->(n:Symptom) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        elif question_type == 'disease_accompany':
            cypher_query1 = [
                "MATCH (m:Disease)-[r:accompany_with]->(n:Disease) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
            cypher_query2 = [
                "MATCH (m:Disease)-[r:accompany_with]->(n:Disease) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
            cypher_query = cypher_query1 + cypher_query2

        return cypher_query


if __name__ == '__main__':
    query_generator = QueryGenerator()
