from django.db import transaction
from undrid.models import Faculty, Department  # Replace 'your_app' with your actual app name

# Data mapping of faculty codes to department info (code, name)
faculty_departments = {
    'AGR': [
        ('AEE', 'Department of Agricultural Economics & Ext. Services'),
        ('ANS', 'Department of Animal Science'),
        ('CRS', 'Department of Crop science'),
        ('FIS', 'Department of Aquaculture and Fisheries Management'),
        ('FOD', 'Department of Food Science and Nutrition'),
        ('FOW', 'Department of Forestry and Wildlife'),
        ('FWM', 'Department of Forest Resources and Wildlife Management'),
        ('SOS', 'Department of Soil Science'),
    ],
    'AIML': [
        ('AIML', 'AFRIMAL'),
    ],
    'ART': [
        ('ENL', 'Department of English and Literature'),
        ('FAA', 'Department of Fine and Applied Art'),
        ('FOL', 'Department of Foreign Languages'),
        ('HIS', 'Department of History And International Studies'),
        ('LST', 'Department of Linguistics Studies'),
        ('MAC', 'Department of Mass Communication'),
        ('PHL', 'Department of Philosophy'),
        ('REL', 'Department of Religions'),
        ('THR', 'Department of Theatre Arts'),
    ],
    'BCS': [
        ('CHP', 'Department of Chemical Pathology'),
        ('CPT', 'Department of Clinical Pharmacology and Therapeutics'),
        ('HBS', 'Department of Haematology and Blood Transfusion'),
        ('MMP', 'Department of Medical Microbiology and Parasitology'),
        ('PAF', 'Department of Pathology (Anatomic and Forensic Pathology)'),
        ('PAT', 'Department of Pathology (Anatomic and Forensic Pathology)'),
    ],
    'BMS': [
        ('ANA', 'Department of Anatomy'),
        ('MBC', 'Department of Medical Biochemistry'),
        ('MLS', 'Department of Medical Laboratory Science'),
        ('NSC', 'Department of Nursing Sciences'),
        ('PHS', 'Department of Physiology'),
        ('PST', 'Department of Physiotherapy'),
        ('RAD', 'Department of Radiography'),
    ],
    'CBT': [
        ('DCBT', 'CBT Practice Categories'),
    ],
    'CED': [
        ('CED', 'Centre for Entrepreneurship Development'),
    ],
    'CERHI': [
        ('CHT', 'Department of Community Health'),
        ('ECN', 'Department of Economics'),
        ('NUR', 'Department of Nursing'),
        ('OAG', 'Department of Obstetrics and Gynaecology'),
    ],
    'CFPDS': [
        ('FPDS', 'Department of Forensic Programmes and DNA Studies'),
    ],
    'CGS': [
        ('CGS', 'Centre for Gender Studies'),
    ],
    'COEGPE': [
        ('COEGLY', 'Department of Geology'),
        ('COEGPHY', 'Department of Geophysics'),
        ('COEPEE', 'Department of Petroleum Engineering'),
    ],
    'COEW': [
        ('COEWCSC', 'Department of Computer Science'),
        ('COEWENL', 'Department of English and Literature'),
        ('COEWPGD', 'College of Education Warri PGD'),
    ],
    'CPGE': [
        ('CPP', 'Department of Chemical and Process Engineering, PTI Campus'),
        ('EEP', 'Department of Electric/Electronics Engineering, PTI Campus'),
        ('GEP', 'Department of Gas Engineering, PTI Campus'),
        ('IEP', 'Department of Industrial and Environemntal Engineering, PTI, Campus'),
        ('MEP', 'Department of Mechanical Engineering, PTI Campus'),
        ('PEP', 'Department of Petroleum Engineering, PTI Campus'),
    ],
    'DCOEM': [
        ('COEMPGD', 'College of Education Mosogar PGD (COEMPGD)'),
        ('SOASS', 'School of Arts and Social Sciences'),
        ('SOEDU', 'School of Education'),
        ('SOSCN', 'School of Sciences'),
        ('SOVOC', 'School of Vocation'),
    ],
    'DEN': [
        ('DPV', 'Department of Preventive Dentistry'),
        ('ODR', 'Department of Oral Diagnosis & Maxillofacial Radiology'),
        ('OMPM', 'Department of Oral & Maxillofacial Pathology and Medicine'),
        ('OSP', 'Department of Oral & Maxillofacial Surgery (OMS)'),
        ('PER', 'Department of Periodontics'),
        ('RES', 'Department of Restorative Dentistry'),
    ],
    'EDU': [
        ('ADT', 'Department of Continuing Education and Development Studies'),
        ('CIT', 'Department of Curriculum and Instructional Technology'),
        ('DEF', 'Department of Educational Foundations'),
        ('DEM', 'Department of Educational Management'),
        ('EECP', 'Department of Educational Evaluation and Counselling Psychology'),
        ('EPCS', 'Department of Educational Psychology & Curr. Studies'),
        ('ESM', 'Department of Educational Studies and Management'),
        ('HEK', 'Department of Health Environmental Education and Human Kinetics'),
        ('HKS', 'Department of Human Kinetics and Sports Science'),
        ('HSE', 'Department of Health, Safety and Environmental Education'),
        ('VTE', 'Department of Vocational & Technical Education'),
    ],
    'ENG': [
        ('AGE', 'Department of Agricultural Engineering'),
        ('AGR', 'Department of Agricultural Engineering'),
        ('CHE', 'Department of Chemical Engineering'),
        ('CPE', 'Department of Computer Engineering'),
        ('CVE', 'Department of Civil Engineering'),
        ('DMIC', 'Centre for Maritime Studies, Information & Communication Technology'),
        ('EEE', 'Department of Electrical/Electronics'),
        ('GME', 'Department of Surveying & Geoinformatics'),
        ('IDE', 'Department of Industrial Engineering'),
        ('IND', 'Department of Industrial Engineering'),
        ('MAR', 'Department of Marine Engineering'),
        ('MAT', 'Department of Materials & Metallurgical Engineering'),
        ('MCH', 'Department of Mechanical Engineering'),
        ('MEE', 'Department of Mechanical Engineering'),
        ('MME', 'Department of Materials & Metallurgical Engineering'),
        ('MRE', 'Department of Marine Engineering'),
        ('MTE', 'Department of Mechatronics Engineering'),
        ('PEE', 'Department of Petroleum Engineering'),
        ('PRE', 'Department of Production Engineering'),
        ('STE', 'Department of Structural Engineering'),
    ],
    'ENV': [
        ('ARC', 'Department of Architecture'),
        ('ESM', 'Department of Estate Management'),
        ('FAA', 'Department of Fine and Applied Arts (ENV)'),
        ('GEM', 'Department of Geomatics'),
        ('QSV', 'Department of Quantity Surveying'),
        ('URP', 'Department of Urban and Regional Planning'),
    ],
    'FCETA': [
        ('SOBUSE', 'School of Business Education'),
        ('SOSCNE', 'School of Science Education'),
        ('SOTECH', 'School of Technical Education'),
        ('SOVOC', 'School of Vocational Education'),
    ],
    'FCETAL': [
        ('ESMA', 'Department of Educational Studies and Management'),
        ('PCSA', 'Department of Psychology and Curriculum Studies'),
        ('VTEA', 'Department of Vocational And Technical Education'),
    ],
    'FLC': [
        ('FLC', 'Fench Language Centre'),
    ],
    'GST': [
        ('GST', 'Department of General Studies'),
    ],
    'ICH': [
        ('CH', 'Institute of Child Health'),
    ],
    'ICSAN': [
        ('ICSAN', 'Institute of Chartered Secretaries and Administrators of Nigeria'),
    ],
    'INE': [
        ('INE', 'Institute of Education'),
    ],
    'INP': [
        ('INP', 'Institute of Public Administration and Health Services Management (IPAHSM)'),
    ],
    'JUPEB': [
        ('AGR_JUP', 'Agriculture-Subjects Combination'),
        ('ART_JUP', 'Arts-Subjects Combination'),
        ('EDU_JUP', 'Education-Subjects Combination'),
        ('ENG_JUP', 'Engineering-Subjects Combination'),
        ('LAW_JUP', 'Law-Subjects Combination'),
        ('LSC_JUP', 'Life Sciences-Subjects Combination'),
        ('MED_JUP', 'Medicine/Dentistry/Pharmacy/BMS-Subjects Combination'),
        ('MGS_JUP', 'Management/Social Sciences-Subjects Combination'),
        ('PSC_JUP', 'Physical Sciences-Subjects Combination'),
        ('SSC_JUP', 'Department of Social Sciences-Subjects Combination'),
    ],
    'JUPEB_AK': [
        ('AGR_JUP_AK', 'Agriculture-Subjects Combination (AGR_JUP)'),
        ('ART_JUP_AK', 'Arts-Subjects Combination (ART_JUP)'),
        ('EDU_JUP_AK', 'Education-Subjects Combination (EDU_JUP)'),
        ('ENG_JUP_AK', 'Engineering-Subjects Combination (ENG_JUP)'),
        ('LAW_JUP_AK', 'Law-Subjects Combination (LAW_JUP)'),
        ('LSC_JUP_AK', 'Life Sciences-Subjects Combination (LSC_JUP)'),
        ('MED_JUP_AK', 'Medicine/Dentistry/Pharmacy/BMS-Subjects Combination (MED_JUP)'),
        ('MGS_JUP_AK', 'Management/Social Sciences-Subjects Combination (MGS_JUP)'),
        ('PSC_JUP_AK', 'Physical Sciences-Subjects Combination (PSC_JUP)'),
    ],
    'LAW': [
        ('BUL', 'Department of Business Law'),
        ('JIL', 'Department of Jurisprudence and International Law'),
        ('LAW', 'Department of Law'),
        ('PPL', 'Department of Private and Property Law'),
        ('PUL', 'Department of Public Law'),
    ],
    'LSC': [
        ('AEB', 'Department of Animal and Environmental Biology'),
        ('AGP', 'Department of Applied Geophysics'),
        ('BCH', 'Department of Biochemistry'),
        ('BOT', 'Department of Botany'),
        ('CED', 'Centre for Enterpreneural Development'),
        ('EMT', 'Department of Environmental Management & Toxicology'),
        ('EVL', 'Department of Enviromental Science'),
        ('MCB', 'Department of Microbiology'),
        ('OPT', 'Department of Optometry'),
        ('PBB', 'Department of Plant Biology and Biotechnology'),
        ('SLT', 'Department of Science Laboratory Technology'),
        ('ZOO', 'Department of Zoology'),
    ],
    'MED': [
        ('ANT', 'Department of Anatomy'),
        ('ANY', 'Department of Anaesthesiology'),
        ('CHH', 'Department of Child Health'),
        ('COH', 'Department of Public Health and Community Medicine'),
        ('HAE', 'Department of Haematology'),
        ('MED', 'Department of Medicine'),
        ('MEH', 'Department of Mental Health'),
        ('PHS', 'Department of Physiology'),
        ('SUR', 'Department of Surgery'),
    ],
    'MGS': [
        ('ACC', 'Department of Accounting'),
        ('ACT', 'Department of Actuarial Science'),
        ('BNK', 'Department of Banking and Finance'),
        ('BUS', 'Department of Business Administration'),
        ('ENT', 'Department of Entrepreneurship'),
        ('FIN', 'Department of Finance'),
        ('HRM', 'Department of Human Resource Management'),
        ('INS', 'Department of Insurance'),
        ('MKT', 'Department of Marketing'),
    ],
    'NILS': [
        ('NILS', 'National Institute for Legislative and Democratic Studies'),
    ],
    'PESRC': [],  # No departments listed
    'PHA': [
        ('PCG', 'Department of Pharmacognosy'),
        ('PCH', 'Department of Pharmaceutical Chemistry'),
        ('PCN', 'Department of Clinical Pharmacy & Pharmacy Practice'),
        ('PCO', 'Department of Pharmacology and Toxicology'),
        ('PCT', 'Department of Pharmaceutics & Pharmaceutical Technology'),
        ('PHA', 'Department of Pharmacy'),
        ('PHM', 'Department of Pharmaceutical Mathematics'),
        ('PMB', 'Department of Pharmaceutical Microbiology and Biotechnology'),
    ],
    'PSC': [
        ('CHM', 'Department of Chemistry'),
        ('CSC', 'Department of Computer Science'),
        ('GLY', 'Department of Geology'),
        ('MTH', 'Department of Mathematics'),
        ('PHY', 'Department of Physics'),
    ],
}


@transaction.atomic
def populate_departments():
    # Counter for statistics
    created_count = 0
    skipped_count = 0
    error_count = 0

    print("Starting department population...")

    for faculty_code, departments in faculty_departments.items():
        try:
            # Get the faculty by code
            try:
                faculty = Faculty.objects.get(code=faculty_code)
                print(f"Found faculty: {faculty.title} ({faculty_code})")
            except Faculty.DoesNotExist:
                print(f"Warning: Faculty with code {faculty_code} not found. Skipping its departments.")
                skipped_count += len(departments)
                continue

            # Create each department for this faculty
            for dept_code, dept_name in departments:
                try:
                    # Check if department already exists
                    dept, created = Department.objects.get_or_create(
                        code=dept_code,
                        faculty=faculty,
                        defaults={'title': dept_name}
                    )

                    if created:
                        print(f"Created department: {dept_name} ({dept_code})")
                        created_count += 1
                    else:
                        print(f"Department already exists: {dept_name} ({dept_code})")
                        skipped_count += 1

                except Exception as e:
                    print(f"Error creating department {dept_code}: {str(e)}")
                    error_count += 1

        except Exception as e:
            print(f"Error processing faculty {faculty_code}: {str(e)}")
            error_count += 1

    print("\nPopulation complete!")
    print(f"Departments created: {created_count}")
    print(f"Departments skipped: {skipped_count}")
    print(f"Errors encountered: {error_count}")

    return created_count, skipped_count, error_count


if __name__ == "__main__":
    # This allows the script to be run directly with python manage.py shell < this_script.py
    populate_departments()