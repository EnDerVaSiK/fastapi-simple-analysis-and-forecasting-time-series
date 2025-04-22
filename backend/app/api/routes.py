from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from backend.app.services.forecasting import ForecastService
from backend.app.models.dataset import CSVDataset
import os
import logging

router = APIRouter()
logger = logging.getLogger(__name__)
service = ForecastService()


@router.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    try:
        if not file.filename.endswith('.csv'):
            raise ValueError("Only CSV files allowed")

        # Сохранение файла
        file_path = f"uploads/{file.filename}"
        os.makedirs("uploads", exist_ok=True)

        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        # Обработка и прогнозирование
        dataset = service.prepare_data(file_path)
        result = service.make_forecast(dataset)

        return JSONResponse(
            content={
                "status": "success",
                "forecast": result["forecast"],
                "filename": file.filename
            },
            media_type="application/json; charset=utf-8"
        )

    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        raise HTTPException(400, detail=str(e))
