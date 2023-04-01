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
        sqls = []
        for question_type in question_types:
            sql_ = {}
            sql_['question_type'] = question_type
            sql = []
            if question_type == 'disease_symptom':
                sql = self.generate_sql(
                    question_type, entity_dict.get('disease'))

            elif question_type == 'symptom_disease':
                sql = self.generate_sql(
                    question_type, entity_dict.get('symptom'))

            elif question_type == 'disease_cause':
                sql = self.generate_sql(
                    question_type, entity_dict.get('disease'))

            elif question_type == 'disease_acompany':
                sql = self.generate_sql(
                    question_type, entity_dict.get('disease'))

            elif question_type == 'disease_prevent':
                sql = self.generate_sql(
                    question_type, entity_dict.get('disease'))

            elif question_type == 'disease_lasttime':
                sql = self.generate_sql(
                    question_type, entity_dict.get('disease'))

            elif question_type == 'disease_cureway':
                sql = self.generate_sql(
                    question_type, entity_dict.get('disease'))

            elif question_type == 'disease_cureprob':
                sql = self.generate_sql(
                    question_type, entity_dict.get('disease'))

            elif question_type == 'disease_easyget':
                sql = self.generate_sql(
                    question_type, entity_dict.get('disease'))

            elif question_type == 'disease_desc':
                sql = self.generate_sql(
                    question_type, entity_dict.get('disease'))

            if sql:
                sql_['sql'] = sql

                sqls.append(sql_)

        return sqls

    def generate_sql(self, question_type, entities):
        if not entities:
            return []

        sql = []

        if question_type == 'disease_cause':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.cause".format(
                i) for i in entities]

        elif question_type == 'disease_prevent':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.prevent".format(
                i) for i in entities]

        elif question_type == 'disease_lasttime':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.cure_lasttime".format(
                i) for i in entities]

        elif question_type == 'disease_cureprob':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.cured_prob".format(
                i) for i in entities]

        elif question_type == 'disease_cureway':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.cure_way".format(
                i) for i in entities]

        elif question_type == 'disease_easyget':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.easy_get".format(
                i) for i in entities]

        elif question_type == 'disease_desc':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.desc".format(
                i) for i in entities]

        elif question_type == 'disease_symptom':
            sql = [
                "MATCH (m:Disease)-[r:has_symptom]->(n:Symptom) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        elif question_type == 'symptom_disease':
            sql = [
                "MATCH (m:Disease)-[r:has_symptom]->(n:Symptom) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        elif question_type == 'disease_accompany':
            sql1 = [
                "MATCH (m:Disease)-[r:accompany_with]->(n:Disease) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
            sql2 = [
                "MATCH (m:Disease)-[r:accompany_with]->(n:Disease) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
            sql = sql1 + sql2

        return sql


if __name__ == '__main__':
    query_generator = QueryGenerator()
