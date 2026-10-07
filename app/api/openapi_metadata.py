# Metadatos y respuestas reutilizables para la documentación OpenAPI.

OPENAPI_METADATA = {
	"title": "Palmeras en la Mancha Records API",
	"description": (
		"API para consultar y gestionar los recursos de Palmeras en la Mancha Records. "
		"Las operaciones se organizan mediante etiquetas y documentan sus respuestas."
	),
	"version": "1.0.0",
	"openapi_tags": [
		{"name": "Health", "description": "Comprobaciones de disponibilidad del servicio."},
		{"name": "Records", "description": "Operaciones para consultar y gestionar registros."},
	],
}

# Respuestas reutilizables en el parámetro ``responses`` de los decoradores FastAPI.
OPENAPI_RESPONSES = {
	400: {
		"description": "La solicitud contiene datos no válidos.",
		"content": {"application/json": {"example": {"detail": "Solicitud no válida"}}},
	},
	404: {
		"description": "No se encontró el recurso solicitado.",
		"content": {"application/json": {"example": {"detail": "Recurso no encontrado"}}},
	},
	422: {
		"description": "Los datos de entrada no superan la validación.",
		"content": {
			"application/json": {
				"example": {
					"detail": [
						{"loc": ["body", "field"], "msg": "Field required", "type": "missing"}
					]
				}
			}
		},
	},
	500: {
		"description": "Se produjo un error inesperado en el servidor.",
		"content": {"application/json": {"example": {"detail": "Error interno del servidor"}}},
	},
}
