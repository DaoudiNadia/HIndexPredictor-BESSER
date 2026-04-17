import uvicorn
import os, json
import time as time_module
import logging
from fastapi import Depends, FastAPI, HTTPException, Request, status, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from pydantic_classes import *
from sql_alchemy import *

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

############################################
#
#   Initialize the database
#
############################################

def init_db():
    SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/Class_Diagram.db")
    # Ensure local SQLite directory exists (safe no-op for other DBs)
    os.makedirs("data", exist_ok=True)
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        echo=False
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    return SessionLocal

app = FastAPI(
    title="Class_Diagram API",
    description="Auto-generated REST API with full CRUD operations, relationship management, and advanced features",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {"name": "System", "description": "System health and statistics"},
        {"name": "Researcher", "description": "Operations for Researcher entities"},
        {"name": "Researcher Relationships", "description": "Manage Researcher relationships"},
        {"name": "Researcher Methods", "description": "Execute Researcher methods"},
        {"name": "ResearchField", "description": "Operations for ResearchField entities"},
        {"name": "ResearchField Relationships", "description": "Manage ResearchField relationships"},
    ]
)

# Enable CORS for all origins (for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict to ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

############################################
#
#   Middleware
#
############################################

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests and responses."""
    logger.info(f"Incoming request: {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time header to all responses."""
    start_time = time_module.time()
    response = await call_next(request)
    process_time = time_module.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

############################################
#
#   Exception Handlers
#
############################################

# Global exception handlers
@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """Handle ValueError exceptions."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Bad Request",
            "message": str(exc),
            "detail": "Invalid input data provided"
        }
    )


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    """Handle database integrity errors."""
    logger.error(f"Database integrity error: {exc}")

    # Extract more detailed error information
    error_detail = str(exc.orig) if hasattr(exc, 'orig') else str(exc)

    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "error": "Conflict",
            "message": "Data conflict occurred",
            "detail": error_detail
        }
    )


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError):
    """Handle general SQLAlchemy errors."""
    logger.error(f"Database error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": "Database operation failed",
            "detail": "An internal database error occurred"
        }
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions with consistent format."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail if isinstance(exc.detail, str) else "HTTP Error",
            "message": exc.detail,
            "detail": f"HTTP {exc.status_code} error occurred"
        }
    )

# Initialize database session
SessionLocal = init_db()
# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        logger.error("Database session rollback due to exception")
        raise
    finally:
        db.close()

############################################
#
#   Global API endpoints
#
############################################

@app.get("/", tags=["System"])
def root():
    """Root endpoint - API information"""
    return {
        "name": "Class_Diagram API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health", tags=["System"])
def health_check():
    """Health check endpoint for monitoring"""
    from datetime import datetime
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database": "connected"
    }


@app.get("/statistics", tags=["System"])
def get_statistics(database: Session = Depends(get_db)):
    """Get database statistics for all entities"""
    stats = {}
    stats["researcher_count"] = database.query(Researcher).count()
    stats["researchfield_count"] = database.query(ResearchField).count()
    stats["total_entities"] = sum(stats.values())
    return stats


############################################
#
#   BESSER Action Language standard lib
#
############################################


async def BAL_size(sequence:list) -> int:
    return len(sequence)

async def BAL_is_empty(sequence:list) -> bool:
    return len(sequence) == 0

async def BAL_add(sequence:list, elem) -> None:
    sequence.append(elem)

async def BAL_remove(sequence:list, elem) -> None:
    sequence.remove(elem)

async def BAL_contains(sequence:list, elem) -> bool:
    return elem in sequence

async def BAL_filter(sequence:list, predicate) -> list:
    return [elem for elem in sequence if predicate(elem)]

async def BAL_forall(sequence:list, predicate) -> bool:
    for elem in sequence:
        if not predicate(elem):
            return False
    return True

async def BAL_exists(sequence:list, predicate) -> bool:
    for elem in sequence:
        if predicate(elem):
            return True
    return False

async def BAL_one(sequence:list, predicate) -> bool:
    found = False
    for elem in sequence:
        if predicate(elem):
            if found:
                return False
            found = True
    return found

async def BAL_is_unique(sequence:list, mapping) -> bool:
    mapped = [mapping(elem) for elem in sequence]
    return len(set(mapped)) == len(mapped)

async def BAL_map(sequence:list, mapping) -> list:
    return [mapping(elem) for elem in sequence]

async def BAL_reduce(sequence:list, reduce_fn, aggregator) -> any:
    for elem in sequence:
        aggregator = reduce_fn(aggregator, elem)
    return aggregator


############################################
#
#   Researcher functions
#
############################################

@app.get("/researcher/", response_model=None, tags=["Researcher"])
def get_all_researcher(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Researcher)
        query = query.options(joinedload(Researcher.researchfield))
        researcher_list = query.all()

        # Serialize with relationships included
        result = []
        for researcher_item in researcher_list:
            item_dict = researcher_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if researcher_item.researchfield:
                related_obj = researcher_item.researchfield
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['researchfield'] = related_dict
            else:
                item_dict['researchfield'] = None


            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Researcher).all()


@app.get("/researcher/count/", response_model=None, tags=["Researcher"])
def get_count_researcher(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Researcher entities"""
    count = database.query(Researcher).count()
    return {"count": count}


@app.get("/researcher/paginated/", response_model=None, tags=["Researcher"])
def get_paginated_researcher(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Researcher entities"""
    total = database.query(Researcher).count()
    researcher_list = database.query(Researcher).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": researcher_list
    }


@app.get("/researcher/search/", response_model=None, tags=["Researcher"])
def search_researcher(
    database: Session = Depends(get_db)
) -> list:
    """Search Researcher entities by attributes"""
    query = database.query(Researcher)


    results = query.all()
    return results


@app.get("/researcher/{researcher_id}/", response_model=None, tags=["Researcher"])
async def get_researcher(researcher_id: int, database: Session = Depends(get_db)) -> Researcher:
    db_researcher = database.query(Researcher).filter(Researcher.id == researcher_id).first()
    if db_researcher is None:
        raise HTTPException(status_code=404, detail="Researcher not found")

    response_data = {
        "researcher": db_researcher,
}
    return response_data



@app.post("/researcher/", response_model=None, tags=["Researcher"])
async def create_researcher(researcher_data: ResearcherCreate, database: Session = Depends(get_db)) -> Researcher:

    if researcher_data.researchfield is not None:
        db_researchfield = database.query(ResearchField).filter(ResearchField.id == researcher_data.researchfield).first()
        if not db_researchfield:
            raise HTTPException(status_code=400, detail="ResearchField not found")
    else:
        raise HTTPException(status_code=400, detail="ResearchField ID is required")

    db_researcher = Researcher(
        totalPapers=researcher_data.totalPapers,        careerAge=researcher_data.careerAge,        citationsPerPaper=researcher_data.citationsPerPaper,        hIndex=researcher_data.hIndex,        totalCitations=researcher_data.totalCitations,        researchfield_id=researcher_data.researchfield        )

    database.add(db_researcher)
    database.commit()
    database.refresh(db_researcher)




    return db_researcher


@app.post("/researcher/bulk/", response_model=None, tags=["Researcher"])
async def bulk_create_researcher(items: list[ResearcherCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Researcher entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.researchfield:
                raise ValueError("ResearchField ID is required")

            db_researcher = Researcher(
                totalPapers=item_data.totalPapers,                careerAge=item_data.careerAge,                citationsPerPaper=item_data.citationsPerPaper,                hIndex=item_data.hIndex,                totalCitations=item_data.totalCitations,                researchfield_id=item_data.researchfield            )
            database.add(db_researcher)
            database.flush()  # Get ID without committing
            created_items.append(db_researcher.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Researcher entities"
    }


@app.delete("/researcher/bulk/", response_model=None, tags=["Researcher"])
async def bulk_delete_researcher(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Researcher entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_researcher = database.query(Researcher).filter(Researcher.id == item_id).first()
        if db_researcher:
            database.delete(db_researcher)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Researcher entities"
    }

@app.put("/researcher/{researcher_id}/", response_model=None, tags=["Researcher"])
async def update_researcher(researcher_id: int, researcher_data: ResearcherCreate, database: Session = Depends(get_db)) -> Researcher:
    db_researcher = database.query(Researcher).filter(Researcher.id == researcher_id).first()
    if db_researcher is None:
        raise HTTPException(status_code=404, detail="Researcher not found")

    setattr(db_researcher, 'totalPapers', researcher_data.totalPapers)
    setattr(db_researcher, 'careerAge', researcher_data.careerAge)
    setattr(db_researcher, 'citationsPerPaper', researcher_data.citationsPerPaper)
    setattr(db_researcher, 'hIndex', researcher_data.hIndex)
    setattr(db_researcher, 'totalCitations', researcher_data.totalCitations)
    if researcher_data.researchfield is not None:
        db_researchfield = database.query(ResearchField).filter(ResearchField.id == researcher_data.researchfield).first()
        if not db_researchfield:
            raise HTTPException(status_code=400, detail="ResearchField not found")
        setattr(db_researcher, 'researchfield_id', researcher_data.researchfield)
    database.commit()
    database.refresh(db_researcher)

    return db_researcher


@app.delete("/researcher/{researcher_id}/", response_model=None, tags=["Researcher"])
async def delete_researcher(researcher_id: int, database: Session = Depends(get_db)):
    db_researcher = database.query(Researcher).filter(Researcher.id == researcher_id).first()
    if db_researcher is None:
        raise HTTPException(status_code=404, detail="Researcher not found")
    database.delete(db_researcher)
    database.commit()
    return db_researcher



############################################
#   Researcher Method Endpoints
############################################




@app.post("/researcher/{researcher_id}/methods/predict/", response_model=None, tags=["Researcher Methods"])
async def execute_researcher_predict(
    researcher_id: int,
    params: dict = Body(default=None, embed=True),
    database: Session = Depends(get_db)
):
    """
    Execute the predict method on a Researcher instance.
    """
    # Retrieve the entity from the database
    _researcher_object = database.query(Researcher).filter(Researcher.id == researcher_id).first()
    if _researcher_object is None:
        raise HTTPException(status_code=404, detail="Researcher not found")

    # Prepare method parameters

    # Execute the method
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output
        async def wrapper(_researcher_object):
            parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            if parent_dir not in sys.path:
                sys.path.insert(0, parent_dir)
            from nn.nn_inference import predict_hindex
            predicted = predict_hindex(_researcher_object)
            field = database.get(ResearchField, _researcher_object.researchfield_id)
            field_avg = field.averageHIndex if field else None
            field_name = field.name.value if field else "Unknown"
            result = f"Your predicted H-Index in 5 years is {predicted}. The average H-Index in {field_name} is {field_avg}."
            return result


        result = await wrapper(_researcher_object)
        # Commit DB
        database.commit()
        database.refresh(_researcher_object)

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        return {
            "researcher_id": researcher_id,
            "method": "predict",
            "status": "executed",
            "result": str(result) if result is not None else None,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")



############################################
#
#   ResearchField functions
#
############################################

@app.get("/researchfield/", response_model=None, tags=["ResearchField"])
def get_all_researchfield(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(ResearchField)
        researchfield_list = query.all()

        # Serialize with relationships included
        result = []
        for researchfield_item in researchfield_list:
            item_dict = researchfield_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)

            # Add many-to-many and one-to-many relationship objects (full details)
            researcher_list = database.query(Researcher).filter(Researcher.researchfield_id == researchfield_item.id).all()
            item_dict['researcher'] = []
            for researcher_obj in researcher_list:
                researcher_dict = researcher_obj.__dict__.copy()
                researcher_dict.pop('_sa_instance_state', None)
                item_dict['researcher'].append(researcher_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(ResearchField).all()


@app.get("/researchfield/count/", response_model=None, tags=["ResearchField"])
def get_count_researchfield(database: Session = Depends(get_db)) -> dict:
    """Get the total count of ResearchField entities"""
    count = database.query(ResearchField).count()
    return {"count": count}


@app.get("/researchfield/paginated/", response_model=None, tags=["ResearchField"])
def get_paginated_researchfield(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of ResearchField entities"""
    total = database.query(ResearchField).count()
    researchfield_list = database.query(ResearchField).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": researchfield_list
        }

    result = []
    for researchfield_item in researchfield_list:
        researcher_ids = database.query(Researcher.id).filter(Researcher.researchfield_id == researchfield_item.id).all()
        item_data = {
            "researchfield": researchfield_item,
            "researcher_ids": [x[0] for x in researcher_ids]        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/researchfield/search/", response_model=None, tags=["ResearchField"])
def search_researchfield(
    database: Session = Depends(get_db)
) -> list:
    """Search ResearchField entities by attributes"""
    query = database.query(ResearchField)


    results = query.all()
    return results


@app.get("/researchfield/{researchfield_id}/", response_model=None, tags=["ResearchField"])
async def get_researchfield(researchfield_id: int, database: Session = Depends(get_db)) -> ResearchField:
    db_researchfield = database.query(ResearchField).filter(ResearchField.id == researchfield_id).first()
    if db_researchfield is None:
        raise HTTPException(status_code=404, detail="ResearchField not found")

    researcher_ids = database.query(Researcher.id).filter(Researcher.researchfield_id == db_researchfield.id).all()
    response_data = {
        "researchfield": db_researchfield,
        "researcher_ids": [x[0] for x in researcher_ids]}
    return response_data



@app.post("/researchfield/", response_model=None, tags=["ResearchField"])
async def create_researchfield(researchfield_data: ResearchFieldCreate, database: Session = Depends(get_db)) -> ResearchField:


    db_researchfield = ResearchField(
        averageHIndex=researchfield_data.averageHIndex,        name=researchfield_data.name.value        )

    database.add(db_researchfield)
    database.commit()
    database.refresh(db_researchfield)

    if researchfield_data.researcher:
        # Validate that all Researcher IDs exist
        for researcher_id in researchfield_data.researcher:
            db_researcher = database.query(Researcher).filter(Researcher.id == researcher_id).first()
            if not db_researcher:
                raise HTTPException(status_code=400, detail=f"Researcher with id {researcher_id} not found")

        # Update the related entities with the new foreign key
        database.query(Researcher).filter(Researcher.id.in_(researchfield_data.researcher)).update(
            {Researcher.researchfield_id: db_researchfield.id}, synchronize_session=False
        )
        database.commit()



    researcher_ids = database.query(Researcher.id).filter(Researcher.researchfield_id == db_researchfield.id).all()
    response_data = {
        "researchfield": db_researchfield,
        "researcher_ids": [x[0] for x in researcher_ids]    }
    return response_data


@app.post("/researchfield/bulk/", response_model=None, tags=["ResearchField"])
async def bulk_create_researchfield(items: list[ResearchFieldCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple ResearchField entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_researchfield = ResearchField(
                averageHIndex=item_data.averageHIndex,                name=item_data.name.value            )
            database.add(db_researchfield)
            database.flush()  # Get ID without committing
            created_items.append(db_researchfield.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} ResearchField entities"
    }


@app.delete("/researchfield/bulk/", response_model=None, tags=["ResearchField"])
async def bulk_delete_researchfield(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple ResearchField entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_researchfield = database.query(ResearchField).filter(ResearchField.id == item_id).first()
        if db_researchfield:
            database.delete(db_researchfield)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} ResearchField entities"
    }

@app.put("/researchfield/{researchfield_id}/", response_model=None, tags=["ResearchField"])
async def update_researchfield(researchfield_id: int, researchfield_data: ResearchFieldCreate, database: Session = Depends(get_db)) -> ResearchField:
    db_researchfield = database.query(ResearchField).filter(ResearchField.id == researchfield_id).first()
    if db_researchfield is None:
        raise HTTPException(status_code=404, detail="ResearchField not found")

    setattr(db_researchfield, 'averageHIndex', researchfield_data.averageHIndex)
    setattr(db_researchfield, 'name', researchfield_data.name.value)
    if researchfield_data.researcher is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(Researcher).filter(Researcher.researchfield_id == db_researchfield.id).update(
            {Researcher.researchfield_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if researchfield_data.researcher:
            # Validate that all IDs exist
            for researcher_id in researchfield_data.researcher:
                db_researcher = database.query(Researcher).filter(Researcher.id == researcher_id).first()
                if not db_researcher:
                    raise HTTPException(status_code=400, detail=f"Researcher with id {researcher_id} not found")

            # Update the related entities with the new foreign key
            database.query(Researcher).filter(Researcher.id.in_(researchfield_data.researcher)).update(
                {Researcher.researchfield_id: db_researchfield.id}, synchronize_session=False
            )
    database.commit()
    database.refresh(db_researchfield)

    researcher_ids = database.query(Researcher.id).filter(Researcher.researchfield_id == db_researchfield.id).all()
    response_data = {
        "researchfield": db_researchfield,
        "researcher_ids": [x[0] for x in researcher_ids]    }
    return response_data


@app.delete("/researchfield/{researchfield_id}/", response_model=None, tags=["ResearchField"])
async def delete_researchfield(researchfield_id: int, database: Session = Depends(get_db)):
    db_researchfield = database.query(ResearchField).filter(ResearchField.id == researchfield_id).first()
    if db_researchfield is None:
        raise HTTPException(status_code=404, detail="ResearchField not found")
    database.delete(db_researchfield)
    database.commit()
    return db_researchfield







############################################
# Maintaining the server
############################################
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



