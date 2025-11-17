class MonitoringPayloadPresenter:
    @staticmethod
    def to_response(payload):
        return {
            "id": payload.id,
            "monitoring_unit_id": payload.monitoring_unit_id,
            "air_conditioner_id": payload.air_conditioner_id,
            "timestamp": payload.timestamp,
            "temperature": payload.temperature,
            "humidity": payload.humidity,
            "voltage": payload.voltage,
            "current": payload.current,
            "power_consumption": payload.power_consumption,
            "extra_data": payload.extra_data,
        }
