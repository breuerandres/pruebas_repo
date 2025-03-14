from fastapi import HTTPException


def add_model(db, model):
    try:
        db.add(model)
        db.commit()
        db.refresh(model)
        return model
    except:
        raise HTTPException(
            status_code=400, detail="No se pudo agregar a la base de datos")


def get_model_by_attribute(db, model, att, value):
    try:
        return db.query(model).filter(att == value).first()
    except:
        raise HTTPException(
            status_code=400, detail="No se pudo obtener de la base de datos")


def get_all_models_by_attribute(db, model, att, value):
    try:
        return db.query(model).filter(att == value).all()
    except:
        raise HTTPException(
            status_code=400, detail="No se pudo obtener de la base de datos")
