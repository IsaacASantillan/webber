import logging
from faker import Faker
from app import db, MassSpectral, app
from create_terp_dict import terp_dict, terp_dict_length

def clear_massspectral_table():
    db.session.query(MassSpectral).delete()
    db.session.commit()

def create_massspectral():
    for i in range(0, terp_dict_length-1):
        individual_ms = MassSpectral(
                name = terp_dict["Name"][i],
                rt1 = terp_dict["RT1-A"][i],
                rt2 = terp_dict["RT2-A"][i],
                suspected_matches = terp_dict["Suspected_matches"][i],
                formula = terp_dict["Formula"][i],
                mw = terp_dict["MW"][i],
                exactmass = terp_dict["ExactMass"][i],
                casnumber = terp_dict["CAS#"][i],
                derivatization_agent = terp_dict["Derivatization_Agent"][i],
                #comments = terp_dict["Comments"][i],
                retention_index = terp_dict["Retention_index"][i],
                num_peaks = terp_dict["Num Peaks"][i],
                #x_values = terp_dict["X-Values"][i],
                #y_values = terp_dict["Y-Values"][i],
                description= terp_dict["Description"][i],
                db_number = terp_dict["DB#"][i],
                synon = terp_dict["Synon"][i]
            )
        db.session.add(individual_ms)
    db.session.commit()



if __name__ == '__main__':
    with app.app_context():
        logging.info("Creating all tables...")
        clear_massspectral_table()
        create_massspectral()
