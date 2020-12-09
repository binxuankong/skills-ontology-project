skills_query = """
select s."Name" 
from "Skills" s
"""

jobs_query = """
select Job_Title, Company, Salary, Location, Date_Posted, Description, Job_URL, Keywords_Present, Title_Keywords
from {} j
where j.Country = 'Malaysia'
"""