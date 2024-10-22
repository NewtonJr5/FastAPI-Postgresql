from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional, Annotated

import models

from database import SessionLocal, engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class MaquinaBase(BaseModel):
    # codigo: int
    funcao: str

class Manutencao_maquinaBase(BaseModel):
    manutencao_codigo_manutencao: int
    maquina_codigo: int
    data_inicio: str
    data_fim: str

class ManutencaoBase(BaseModel):
    # codigo_manutencao: int
    tipo: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# CRUD máquina
@app.post("/maquina/")
async def create_maquina(maquina: MaquinaBase, db: db_dependency):
        try:
            db.begin()
            db_maquina = models.Maquina(**maquina.dict())
            db.add(db_maquina)
            db.flush()
            db.refresh(db_maquina)
            db.commit()
            return db_maquina
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail="Database error: " + str(e))


@app.get("/maquina/{maquina_id}")
async def read_maquina(maquina_id: int, db: db_dependency):
        try:
            db.begin()
            db_maquina = db.query(models.Maquina).filter(models.Maquina.codigo == maquina_id).first()
            if db_maquina is None:
                raise HTTPException(status_code=404, detail="Maquina not found")
            return db_maquina
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail="Database error: " + str(e))


@app.put("/maquina/{maquina_id}")
async def update_maquina(maquina_id: int, maquina: MaquinaBase, db: db_dependency):
    try:
        db.begin()
        db_maquina = db.query(models.Maquina).filter(models.Maquina.codigo == maquina_id).first()

        if db_maquina is None:
            raise HTTPException(status_code=404, detail="Maquina not found")
        
        db_maquina.funcao = maquina.funcao
        db.commit()
        db.refresh(db_maquina)
        return db_maquina
    
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
        

@app.delete("/maquina/{maquina_id}")
async def delete_maquina(maquina_id: int, db: db_dependency):
        try:
            db.begin()
            db.commit()
            db_maquina = db.query(models.Maquina).filter(models.Maquina.codigo == maquina_id).first()
            if db_maquina is None:
                raise HTTPException(status_code=404, detail="Maquina not found")
            db.delete(db_maquina)
            return db_maquina
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail="Database error: " + str(e))

# CRUD manutenção
@app.post("/manutencao/")
async def create_manutencao(manutencao: ManutencaoBase, db: db_dependency):
    try:
        db.begin()
        db_manutencao = models.Manutencao(**manutencao.dict())
        db.add(db_manutencao)
        db.flush()
        db.refresh(db_manutencao)
        db.commit()
        return db_manutencao
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error: " + str(e))

@app.get("/manutencao/{manutencao_id}")
async def read_manutencao(manutencao_id: int, db: db_dependency):
    try:
        db.begin()
        db_manutencao = db.query(models.Manutencao).filter(models.Manutencao.codigo_manutencao == manutencao_id).first()
        if db_manutencao is None:
            raise HTTPException(status_code=404, detail="Maquina not found")
        return db_manutencao
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    

@app.put("/manutencao/{manutencao_id}")
async def update_manutencao(manutencao_id: int, manutencao: ManutencaoBase, db: db_dependency):
    try:
        db.begin()
        db_manutencao = db.query(models.Manutencao).filter(models.Manutencao.codigo_manutencao == manutencao_id).first()
        if db_manutencao is None:
            raise HTTPException(status_code=404, detail="Maquina not found")
        db_manutencao.tipo = manutencao.tipo
        db.commit()
        db.refresh(db_manutencao)
        return db_manutencao
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
        

@app.delete("/manutencao/{manutencao_id}")
async def delete_manutencao(manutencao_id: int, db: db_dependency):
    try:
        db.begin()
        db_manutencao = db.query(models.Manutencao).filter(models.Manutencao.codigo_manutencao == manutencao_id).first()
        if db_manutencao is None:
            raise HTTPException(status_code=404, detail="Maquina not found")
        db.delete(db_manutencao)
        db.commit()
        return db_manutencao
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    

# CRUD relação manutenção-máquina
@app.post("/manutencao_maquina/")
async def create_manutencao_maquina(manutencao_maquina: Manutencao_maquinaBase, db: db_dependency):
    try:
        db.begin()
        db_manutencao_maquina = models.Manutencao_maquina(**manutencao_maquina.dict())
        db.add(db_manutencao_maquina)
        db.flush()
        db.refresh(db_manutencao_maquina)
        db.commit()
        return db_manutencao_maquina
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error: " + str(e))

@app.get("/manutencao_maquina/{manutencao_id}/{maquina_id}")
async def read_manutencao_maquina(manutencao_id: int, maquina_id: int, db: db_dependency):
    try:
        db.begin()
        db_manutencao_maquina = db.query(models.Manutencao_maquina).filter(models.Manutencao_maquina.manutencao_codigo_manutencao == manutencao_id).filter(models.Manutencao_maquina.maquina_codigo == maquina_id).first()
        if db_manutencao_maquina is None:
            raise HTTPException(status_code=404, detail="Maquina not found")
        return db_manutencao_maquina
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error: " + str(e))

@app.put("/manutencao_maquina/{manutencao_id}/{maquina_id}")
async def update_manutencao_maquina(manutencao_id: int, maquina_id: int, manutencao_maquina: Manutencao_maquinaBase, db: db_dependency):
    try:
        db.begin()
        db_manutencao_maquina = db.query(models.Manutencao_maquina).filter(models.Manutencao_maquina.manutencao_codigo_manutencao == manutencao_id).filter(models.Manutencao_maquina.maquina_codigo == maquina_id).first()
        if db_manutencao_maquina is None:
            raise HTTPException(status_code=404, detail="Maquina not found")
        db_manutencao_maquina.data_inicio = manutencao_maquina.data_inicio
        db_manutencao_maquina.data_fim = manutencao_maquina.data_fim
        db.commit()
        db.refresh(db_manutencao_maquina)
        return db_manutencao_maquina
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error: " + str(e))

@app.delete("/manutencao_maquina/{manutencao_id}/{maquina_id}")
async def delete_manutencao_maquina(manutencao_id: int, maquina_id: int, db: db_dependency):
    try:
        db.begin()
        db_manutencao_maquina = db.query(models.Manutencao_maquina).filter(models.Manutencao_maquina.manutencao_codigo_manutencao == manutencao_id).filter(models.Manutencao_maquina.maquina_codigo == maquina_id).first
        if db_manutencao_maquina is None:
            raise HTTPException(status_code=404, detail="Maquina not found")
        db.delete(db_manutencao_maquina)
        db.commit()
        return db_manutencao_maquina
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error: " + str(e))