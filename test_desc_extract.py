from desc_extract import JobDescriptionExtractor

def test_extractor():
    text = '''Minimum Requirements
2-8+ years experience in Business Intelligence Engineering, Data Engineering, Data Analysis or Data Science roles, building data pipelines and analyzing large datasets to solve problems
Proficiency in SQL and Python
Strong statistical knowledge
Expertise in visualization and using data insights to make recommendations and achieve goals
Proven ability to manage and deliver on multiple projects with great attention to detail
Ability to clearly communicate results and drive impact
Comfortable collaborating across functions to identify data analytics problems and execute solutions with technical rigor and data-driven insights.

Preferred Qualifications
Master’s degree in Mathematics, Statistics, Economics, Engineering, or a related technical field.
Prior experience at a growth stage internet or software company.
Experience with distributed data frameworks like Hadoop and Spark to write and debug data pipelines.
Good understanding of development processes and best practices like engineering standards, code reviews, and testing.
This role is not eligible for hire in the Greater Seattle Area, Greater NYC Area, or San Francisco Bay Area'''
    extractor = JobDescriptionExtractor()
    reqs = extractor.extract_requirements(text)
    for r in reqs:
        print(r)

if __name__ == "__main__":
    test_extractor()
