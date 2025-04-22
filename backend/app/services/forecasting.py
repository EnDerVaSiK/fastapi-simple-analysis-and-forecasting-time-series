import pandas as pd
from prophet import Prophet
from typing import Dict
from backend.app.models.dataset import CSVDataset
from backend.app.models.forecast import ForecastResult
import logging
from io import BytesIO
import matplotlib.pyplot as plt
import base64
from datetime import datetime

logger = logging.getLogger(__name__)


class ForecastService:
    def __init__(self):
        self.model = Prophet(interval_width=0.95)

    def prepare_data(self, file_path: str) -> CSVDataset:
        try:
            df = pd.read_csv(file_path)
            return CSVDataset(
                date_column="ds",
                value_column="y",
                data=df.rename(columns={
                    'date': 'ds',
                    'value': 'y'
                })
            )
        except Exception as e:
            logger.error(f"Data preparation error: {str(e)}")
            raise ValueError("Invalid CSV structure")

    def make_forecast(self, dataset: CSVDataset, periods: int = 30) -> Dict:
        try:
            self.model = Prophet(interval_width=0.95)
            self.model.fit(dataset.data)
            future = self.model.make_future_dataframe(periods=periods)
            forecast = self.model.predict(future)

            # Преобразование Timestamp в строку
            forecast_data = []
            for _, row in forecast.tail(periods).iterrows():
                forecast_data.append(
                    ForecastResult(
                        timestamp=row['ds'].isoformat(),  # Преобразуем в ISO-строку
                        value=round(row['yhat'], 2),
                        confidence_lower=round(row['yhat_lower'], 2),
                        confidence_upper=round(row['yhat_upper'], 2)
                    ).model_dump()
                )

            # Сохранение компонентов
            fig = self.model.plot_components(forecast)
            buf = BytesIO()
            fig.savefig(buf, format='png')
            plt.close(fig)

            return {
                "forecast": {
                    "ds": [str(row['ds']) for _, row in forecast.tail(periods).iterrows()],
                    "yhat": [float(row['yhat']) for _, row in forecast.tail(periods).iterrows()]
                }
            }
        except Exception as e:
            logger.error(f"Forecasting error: {str(e)}")
            raise RuntimeError("Forecast failed")
