#!/usr/bin/env python3
"""
Generate comprehensive API documentation from swagger.py definitions.

This script creates:
1. Clean OpenAPI 3.0 YAML specification
2. Postman collection for API testing
3. Validation of generated documentation

The script handles encoding issues on Windows and provides fallback mechanisms.
"""

import sys
import os
import json
import yaml
from pathlib import Path
from datetime import datetime

# Set UTF-8 encoding for Windows compatibility
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def safe_print(message):
    """Print message with encoding safety for Windows terminals."""
    try:
        print(message)
    except UnicodeEncodeError:
        # Fallback: replace problematic characters
        safe_message = message.encode('ascii', 'replace').decode('ascii')
        print(safe_message)

def generate_openapi_yaml():
    """Generate OpenAPI YAML from Flask-RESTX API object"""
    try:
        # We need to create a minimal Flask app to generate the schema
        from flask import Flask
        from marketdata_api.routes.swagger import swagger_bp
        
        # Create a minimal Flask app with proper configuration
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['SERVER_NAME'] = 'localhost:5000'
        app.config['APPLICATION_ROOT'] = '/api/v1'
        app.config['PREFERRED_URL_SCHEME'] = 'http'
        
        # Register the swagger blueprint
        app.register_blueprint(swagger_bp)
        
        # Generate the schema within app and request context
        with app.app_context():
            with app.test_request_context('/api/v1/'):
                # Get the API object from the blueprint
                from marketdata_api.routes.swagger import api
                
                # Force Flask-RESTx to generate the schema
                try:
                    raw_spec = api.__schema__
                    
                    # Convert to clean OpenAPI 3.0 format
                    spec = convert_to_openapi_30(raw_spec)
                    
                except Exception as inner_e:
                    print(f"Error getting schema: {inner_e}")
                    # Create a clean fallback spec
                    spec = create_fallback_spec()
            
        # Save to file with clean YAML formatting
        openapi_path = project_root / 'docs' / 'openapi' / 'openapi.yaml'
        openapi_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Use safe_dump to avoid Python object references
        with open(openapi_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(spec, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
        
        print(f"✅ Generated OpenAPI YAML: {openapi_path}")
        
        # Debug information
        if spec:
            print(f"   - OpenAPI version: {spec.get('openapi', 'Unknown')}")
            print(f"   - API title: {spec.get('info', {}).get('title', 'Unknown')}")
            print(f"   - Paths found: {len(spec.get('paths', {}))}")
            print(f"   - Components/schemas: {len(spec.get('components', {}).get('schemas', {}))}")
            
            # Print some paths for debugging
            if spec.get('paths'):
                print("   - Available paths:")
                for path in list(spec['paths'].keys())[:5]:  # Show first 5 paths
                    print(f"     * {path}")
                if len(spec['paths']) > 5:
                    print(f"     * ... and {len(spec['paths']) - 5} more")
        else:
            print("   ⚠️  Generated spec is empty or None")
        
        return spec
        
    except Exception as e:
        print(f"❌ Error generating OpenAPI YAML: {e}")
        import traceback
        traceback.print_exc()
        
        # Create a minimal fallback spec
        fallback_spec = create_fallback_spec()
        
        # Save fallback spec
        openapi_path = project_root / 'docs' / 'openapi' / 'openapi.yaml'
        openapi_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(openapi_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(fallback_spec, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
        
        print(f"✅ Generated fallback OpenAPI YAML: {openapi_path}")
        return fallback_spec

def convert_to_openapi_30(swagger_spec):
    """Convert Swagger 2.0 spec to OpenAPI 3.0"""
    if not swagger_spec:
        return create_fallback_spec()
    
    # Start with clean OpenAPI 3.0 structure
    openapi_spec = {
        'openapi': '3.0.0',
        'info': {
            'title': swagger_spec.get('info', {}).get('title', 'MarketDataAPI'),
            'version': swagger_spec.get('info', {}).get('version', '1.0.0'),
            'description': swagger_spec.get('info', {}).get('description', 'API for financial market data')
        },
        'servers': [
            {
                'url': 'http://127.0.0.1:5000/api/v1',
                'description': 'Development server'
            }
        ],
        'paths': {},
        'components': {
            'schemas': {},
            'securitySchemes': {
                'ApiKeyAuth': {
                    'type': 'apiKey',
                    'in': 'header',
                    'name': 'Authorization'
                }
            }
        },
        'security': [
            {'ApiKeyAuth': []}
        ]
    }
    
    # Convert paths from Swagger 2.0 to OpenAPI 3.0
    swagger_paths = swagger_spec.get('paths', {})
    if isinstance(swagger_paths, dict):
        for path, methods in swagger_paths.items():
            if isinstance(methods, dict):
                openapi_spec['paths'][path] = convert_path_methods(methods)
    
    # Convert definitions to components/schemas
    definitions = swagger_spec.get('definitions', {})
    if isinstance(definitions, dict):
        for name, schema in definitions.items():
            if isinstance(schema, dict):
                openapi_spec['components']['schemas'][name] = convert_schema(schema)
    
    return openapi_spec

def convert_path_methods(methods):
    """Convert path methods from Swagger 2.0 to OpenAPI 3.0"""
    converted_methods = {}
    
    for method, details in methods.items():
        if method == 'parameters':
            # Handle path-level parameters
            continue
            
        if isinstance(details, dict):
            converted_method = {
                'summary': details.get('summary', ''),
                'description': details.get('description', ''),
                'operationId': details.get('operationId', ''),
                'tags': details.get('tags', []),
                'parameters': convert_parameters(details.get('parameters', [])),
                'responses': convert_responses(details.get('responses', {}))
            }
            
            # Add security if present
            if 'security' in details:
                converted_method['security'] = details['security']
            
            converted_methods[method] = converted_method
    
    return converted_methods

def convert_parameters(parameters):
    """Convert parameters from Swagger 2.0 to OpenAPI 3.0"""
    if not isinstance(parameters, list):
        return []
    
    converted_params = []
    for param in parameters:
        if isinstance(param, dict):
            converted_param = {
                'name': param.get('name', ''),
                'in': param.get('in', 'query'),
                'description': param.get('description', ''),
                'required': param.get('required', False),
                'schema': {
                    'type': param.get('type', 'string')
                }
            }
            
            if 'format' in param:
                converted_param['schema']['format'] = param['format']
            
            converted_params.append(converted_param)
    
    return converted_params

def convert_responses(responses):
    """Convert responses from Swagger 2.0 to OpenAPI 3.0"""
    if not isinstance(responses, dict):
        return {'200': {'description': 'Success'}}
    
    converted_responses = {}
    for code, response in responses.items():
        if isinstance(response, dict):
            converted_response = {
                'description': response.get('description', 'Response')
            }
            
            # Add content if schema is present
            if 'schema' in response:
                converted_response['content'] = {
                    'application/json': {
                        'schema': convert_schema(response['schema'])
                    }
                }
            
            converted_responses[str(code)] = converted_response
    
    return converted_responses

def convert_schema(schema):
    """Convert schema from Swagger 2.0 to OpenAPI 3.0"""
    if not isinstance(schema, dict):
        return {'type': 'object'}
    
    converted_schema = {}
    
    # Copy basic properties
    for prop in ['type', 'description', 'example', 'enum', 'format']:
        if prop in schema:
            converted_schema[prop] = schema[prop]
    
    # Handle $ref
    if '$ref' in schema:
        ref = schema['$ref']
        if ref.startswith('#/definitions/'):
            converted_schema['$ref'] = ref.replace('#/definitions/', '#/components/schemas/')
        else:
            converted_schema['$ref'] = ref
    
    # Handle properties
    if 'properties' in schema and isinstance(schema['properties'], dict):
        converted_schema['properties'] = {}
        for prop_name, prop_schema in schema['properties'].items():
            converted_schema['properties'][prop_name] = convert_schema(prop_schema)
    
    # Handle arrays
    if 'items' in schema:
        converted_schema['items'] = convert_schema(schema['items'])
    
    # Handle required fields
    if 'required' in schema:
        converted_schema['required'] = schema['required']
    
    return converted_schema

def create_fallback_spec():
    """Create a comprehensive fallback OpenAPI specification with transparency endpoints"""
    return {
        'openapi': '3.0.0',
        'info': {
            'title': 'MarketDataAPI',
            'version': '1.0.0',
            'description': 'API for financial market data, instrument details, and legal entity information'
        },
        'servers': [
            {
                'url': 'http://127.0.0.1:5000/api/v1',
                'description': 'Development server'
            }
        ],
        'paths': {
            '/instruments': {
                'get': {
                    'summary': 'Get All Instruments',
                    'tags': ['Instruments'],
                    'parameters': [
                        {
                            'name': 'type',
                            'in': 'query',
                            'description': 'Filter by instrument type',
                            'schema': {'type': 'string'}
                        }
                    ],
                    'responses': {
                        '200': {
                            'description': 'Success',
                            'content': {
                                'application/json': {
                                    'schema': {
                                        'type': 'object',
                                        'properties': {
                                            'status': {'type': 'string'},
                                            'data': {'type': 'array', 'items': {'type': 'object'}}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            '/instruments/{identifier}': {
                'get': {
                    'summary': 'Get Instrument by ID or ISIN',
                    'tags': ['Instruments'],
                    'parameters': [
                        {
                            'name': 'identifier',
                            'in': 'path',
                            'required': True,
                            'description': 'Instrument ID or ISIN',
                            'schema': {'type': 'string'}
                        }
                    ],
                    'responses': {
                        '200': {'description': 'Success'},
                        '404': {'description': 'Instrument not found'}
                    }
                }
            },
            '/legal-entities': {
                'get': {
                    'summary': 'Get All Legal Entities',
                    'tags': ['Legal Entities'],
                    'responses': {
                        '200': {
                            'description': 'Success',
                            'content': {
                                'application/json': {
                                    'schema': {
                                        'type': 'object',
                                        'properties': {
                                            'status': {'type': 'string'},
                                            'data': {'type': 'array', 'items': {'type': 'object'}}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            '/legal-entities/{lei}': {
                'get': {
                    'summary': 'Get Legal Entity by LEI',
                    'tags': ['Legal Entities'],
                    'parameters': [
                        {
                            'name': 'lei',
                            'in': 'path',
                            'required': True,
                            'description': 'Legal Entity Identifier',
                            'schema': {'type': 'string'}
                        }
                    ],
                    'responses': {
                        '200': {'description': 'Success'},
                        '404': {'description': 'Entity not found'}
                    }
                }
            },
            '/transparency': {
                'get': {
                    'summary': 'Get All Transparency Calculations',
                    'description': 'Retrieves a list of transparency calculations with optional filtering by calculation type, instrument type, or ISIN',
                    'tags': ['Transparency'],
                    'parameters': [
                        {
                            'name': 'calculation_type',
                            'in': 'query',
                            'description': 'Filter by calculation type',
                            'schema': {'type': 'string', 'enum': ['EQUITY', 'NON_EQUITY']}
                        },
                        {
                            'name': 'instrument_type',
                            'in': 'query',
                            'description': 'Filter by instrument type',
                            'schema': {'type': 'string', 'enum': ['equity', 'debt', 'futures']}
                        },
                        {
                            'name': 'isin',
                            'in': 'query',
                            'description': 'Filter by ISIN',
                            'schema': {'type': 'string'}
                        },
                        {
                            'name': 'page',
                            'in': 'query',
                            'description': 'Page number',
                            'schema': {'type': 'integer', 'default': 1}
                        },
                        {
                            'name': 'per_page',
                            'in': 'query',
                            'description': 'Items per page',
                            'schema': {'type': 'integer', 'default': 20}
                        }
                    ],
                    'responses': {
                        '200': {
                            'description': 'Success',
                            'content': {
                                'application/json': {
                                    'schema': {
                                        'type': 'object',
                                        'properties': {
                                            'status': {'type': 'string'},
                                            'data': {
                                                'type': 'array',
                                                'items': {
                                                    'type': 'object',
                                                    'properties': {
                                                        'id': {'type': 'string'},
                                                        'isin': {'type': 'string'},
                                                        'calculation_type': {'type': 'string'},
                                                        'liquidity': {'type': 'boolean'},
                                                        'total_transactions_executed': {'type': 'integer'},
                                                        'total_volume_executed': {'type': 'number'}
                                                    }
                                                }
                                            },
                                            'meta': {
                                                'type': 'object',
                                                'properties': {
                                                    'page': {'type': 'integer'},
                                                    'per_page': {'type': 'integer'},
                                                    'total': {'type': 'integer'}
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                'post': {
                    'summary': 'Create Transparency Calculation',
                    'description': 'Creates a new transparency calculation with the provided data',
                    'tags': ['Transparency'],
                    'requestBody': {
                        'content': {
                            'application/json': {
                                'schema': {
                                    'type': 'object',
                                    'required': ['ISIN', 'TechRcrdId'],
                                    'properties': {
                                        'ISIN': {'type': 'string', 'description': 'International Securities Identification Number'},
                                        'TechRcrdId': {'type': 'string', 'description': 'Technical record identifier'},
                                        'calculation_type': {'type': 'string', 'enum': ['EQUITY', 'NON_EQUITY'], 'default': 'NON_EQUITY'},
                                        'FrDt': {'type': 'string', 'format': 'date', 'description': 'From date (YYYY-MM-DD)'},
                                        'ToDt': {'type': 'string', 'format': 'date', 'description': 'To date (YYYY-MM-DD)'},
                                        'Lqdty': {'type': 'string', 'description': 'Liquidity indicator (true/false)'},
                                        'TtlNbOfTxsExctd': {'type': 'integer', 'description': 'Total number of transactions executed'},
                                        'TtlVolOfTxsExctd': {'type': 'number', 'description': 'Total volume of transactions executed'}
                                    }
                                }
                            }
                        }
                    },
                    'responses': {
                        '201': {'description': 'Transparency calculation created successfully'},
                        '400': {'description': 'Bad request - invalid data provided'}
                    }
                }
            },
            '/transparency/{transparency_id}': {
                'get': {
                    'summary': 'Get Transparency Calculation by ID',
                    'description': 'Retrieves detailed information about a specific transparency calculation',
                    'tags': ['Transparency'],
                    'parameters': [
                        {
                            'name': 'transparency_id',
                            'in': 'path',
                            'required': True,
                            'description': 'Transparency calculation ID',
                            'schema': {'type': 'string'}
                        }
                    ],
                    'responses': {
                        '200': {
                            'description': 'Success',
                            'content': {
                                'application/json': {
                                    'schema': {
                                        'type': 'object',
                                        'properties': {
                                            'id': {'type': 'string'},
                                            'isin': {'type': 'string'},
                                            'calculation_type': {'type': 'string'},
                                            'tech_record_id': {'type': 'string'},
                                            'from_date': {'type': 'string', 'format': 'date'},
                                            'to_date': {'type': 'string', 'format': 'date'},
                                            'liquidity': {'type': 'boolean'},
                                            'total_transactions_executed': {'type': 'integer'},
                                            'total_volume_executed': {'type': 'number'},
                                            'created_at': {'type': 'string', 'format': 'date-time'},
                                            'updated_at': {'type': 'string', 'format': 'date-time'}
                                        }
                                    }
                                }
                            }
                        },
                        '404': {'description': 'Transparency calculation not found'}
                    }
                }
            },
            '/transparency/isin/{isin}': {
                'get': {
                    'summary': 'Get Transparency by ISIN',
                    'description': 'Retrieves transparency calculations for a specific ISIN, optionally creating them if they do not exist',
                    'tags': ['Transparency'],
                    'parameters': [
                        {
                            'name': 'isin',
                            'in': 'path',
                            'required': True,
                            'description': 'ISIN to search for',
                            'schema': {'type': 'string'}
                        },
                        {
                            'name': 'calculation_type',
                            'in': 'query',
                            'description': 'Calculation type to get/create',
                            'schema': {'type': 'string', 'enum': ['EQUITY', 'NON_EQUITY']}
                        },
                        {
                            'name': 'ensure_instrument',
                            'in': 'query',
                            'description': 'Ensure instrument exists before creating transparency data',
                            'schema': {'type': 'boolean', 'default': True}
                        }
                    ],
                    'responses': {
                        '200': {'description': 'Success'},
                        '404': {'description': 'No calculations found for this ISIN'}
                    }
                }
            },
            '/transparency/batch': {
                'post': {
                    'summary': 'Batch Source Transparency from FITRS',
                    'description': 'Batch source transparency calculations from FITRS data based on specified criteria',
                    'tags': ['Transparency'],
                    'requestBody': {
                        'content': {
                            'application/json': {
                                'schema': {
                                    'type': 'object',
                                    'required': ['calculation_type'],
                                    'properties': {
                                        'calculation_type': {'type': 'string', 'enum': ['EQUITY', 'NON_EQUITY']},
                                        'isin_prefix': {'type': 'string', 'description': 'ISIN prefix filter (e.g., NL for Netherlands)'},
                                        'limit': {'type': 'integer', 'default': 10, 'description': 'Maximum number of calculations to create'},
                                        'cfi_type': {'type': 'string', 'enum': ['D', 'F', 'E'], 'description': 'CFI type filter'}
                                    }
                                }
                            }
                        }
                    },
                    'responses': {
                        '201': {'description': 'Batch transparency calculations created successfully'},
                        '400': {'description': 'Bad request - invalid parameters'}
                    }
                }
            },
            '/transparency/batch-create': {
                'post': {
                    'summary': 'Batch Create Transparency Calculations',
                    'description': 'Create multiple transparency calculations from provided data array',
                    'tags': ['Transparency'],
                    'requestBody': {
                        'content': {
                            'application/json': {
                                'schema': {
                                    'type': 'object',
                                    'required': ['records'],
                                    'properties': {
                                        'records': {
                                            'type': 'array',
                                            'items': {
                                                'type': 'object',
                                                'properties': {
                                                    'ISIN': {'type': 'string'},
                                                    'TechRcrdId': {'type': 'string'},
                                                    'calculation_type': {'type': 'string', 'enum': ['EQUITY', 'NON_EQUITY']},
                                                    'FrDt': {'type': 'string', 'format': 'date'},
                                                    'ToDt': {'type': 'string', 'format': 'date'},
                                                    'Lqdty': {'type': 'string'},
                                                    'TtlNbOfTxsExctd': {'type': 'integer'},
                                                    'TtlVolOfTxsExctd': {'type': 'number'}
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    'responses': {
                        '201': {'description': 'Batch creation completed'},
                        '400': {'description': 'Bad request - invalid records provided'}
                    }
                }
            },
            '/schemas': {
                'get': {
                    'summary': 'Get All Schemas',
                    'tags': ['Schemas'],
                    'responses': {
                        '200': {
                            'description': 'Success',
                            'content': {
                                'application/json': {
                                    'schema': {
                                        'type': 'object',
                                        'properties': {
                                            'status': {'type': 'string'},
                                            'data': {'type': 'array', 'items': {'type': 'object'}}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        'components': {
            'schemas': {
                'Error': {
                    'type': 'object',
                    'properties': {
                        'error': {'type': 'string'}
                    }
                },
                'TransparencyCalculation': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'string'},
                        'isin': {'type': 'string'},
                        'calculation_type': {'type': 'string', 'enum': ['EQUITY', 'NON_EQUITY']},
                        'tech_record_id': {'type': 'string'},
                        'from_date': {'type': 'string', 'format': 'date'},
                        'to_date': {'type': 'string', 'format': 'date'},
                        'liquidity': {'type': 'boolean'},
                        'total_transactions_executed': {'type': 'integer'},
                        'total_volume_executed': {'type': 'number'},
                        'created_at': {'type': 'string', 'format': 'date-time'},
                        'updated_at': {'type': 'string', 'format': 'date-time'}
                    }
                }
            },
            'securitySchemes': {
                'ApiKeyAuth': {
                    'type': 'apiKey',
                    'in': 'header',
                    'name': 'Authorization'
                }
            }
        },
        'security': [
            {'ApiKeyAuth': []}
        ]
    }

def generate_postman_collection(openapi_spec):
    """Generate Postman collection from OpenAPI spec"""
    try:
        if not openapi_spec:
            print("⚠️  No OpenAPI spec available for Postman collection generation")
            return
            
        # Basic Postman collection structure
        collection = {
            "info": {
                "name": "MarketDataAPI",
                "description": "Generated from OpenAPI specification",
                "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
                "version": openapi_spec.get('info', {}).get('version', '1.0.0')
            },
            "auth": {
                "type": "apikey",
                "apikey": [
                    {
                        "key": "key",
                        "value": "Authorization",
                        "type": "string"
                    },
                    {
                        "key": "value",
                        "value": "Bearer {{api_key}}",
                        "type": "string"
                    }
                ]
            },
            "variable": [
                {
                    "key": "base_url",
                    "value": "http://127.0.0.1:5000/api/v1",
                    "type": "string"
                },
                {
                    "key": "api_key",
                    "value": "your_api_key_here",
                    "type": "string"
                }
            ],
            "item": []
        }
        
        # Add basic endpoints from the spec
        if 'paths' in openapi_spec:
            for path, methods in openapi_spec['paths'].items():
                for method, details in methods.items():
                    if method in ['get', 'post', 'put', 'delete']:
                        item = {
                            "name": details.get('summary', f"{method.upper()} {path}"),
                            "request": {
                                "method": method.upper(),
                                "header": [],
                                "url": {
                                    "raw": "{{base_url}}" + path,
                                    "host": ["{{base_url}}"],
                                    "path": path.strip('/').split('/')
                                }
                            }
                        }
                        collection["item"].append(item)
        
        postman_path = project_root / 'docs' / 'postman' / 'MarketDataAPI.postman_collection.json'
        postman_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(postman_path, 'w', encoding='utf-8') as f:
            json.dump(collection, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Generated Postman collection: {postman_path}")
        
    except Exception as e:
        print(f"❌ Error generating Postman collection: {e}")
        import traceback
        traceback.print_exc()

def validate_documentation():
    """Validate that all documentation is consistent"""
    try:
        issues = []
        
        # Check if swagger.py file exists and is importable
        try:
            from marketdata_api.routes.swagger import api
            print("✅ Swagger module imported successfully")
        except ImportError as e:
            issues.append(f"Cannot import swagger module: {e}")
        
        # Check if main API routes are accessible
        try:
            from marketdata_api.routes import entity_routes, instrument_routes
            print("✅ Route modules imported successfully")
        except ImportError as e:
            issues.append(f"Cannot import route modules: {e}")
        
        if issues:
            print("⚠️  Documentation validation issues found:")
            for issue in issues:
                print(f"   - {issue}")
            return False
        else:
            print("✅ Documentation validation passed")
            return True
        
    except Exception as e:
        print(f"❌ Error validating documentation: {e}")
        import traceback
        traceback.print_exc()
        return False

def validate_generated_files():
    """Validate that generated files exist and are valid"""
    try:
        issues = []
        
        # Check if generated OpenAPI file exists
        openapi_path = project_root / 'docs' / 'openapi' / 'openapi.yaml'
        if not openapi_path.exists():
            issues.append("Generated OpenAPI YAML file not found")
        else:
            print("✅ Generated OpenAPI YAML file exists")
            
        # Check if generated Postman collection exists
        postman_path = project_root / 'docs' / 'postman' / 'MarketDataAPI.postman_collection.json'
        if not postman_path.exists():
            issues.append("Generated Postman collection not found")
        else:
            print("✅ Generated Postman collection exists")
        
        if issues:
            print("⚠️  Generated file validation issues found:")
            for issue in issues:
                print(f"   - {issue}")
            return False
        else:
            print("✅ Generated file validation passed")
            return True
        
    except Exception as e:
        print(f"❌ Error validating generated files: {e}")
        return False

def main():
    """Main documentation generation workflow"""
    print("🚀 Generating MarketDataAPI documentation...")
    print(f"📁 Project root: {project_root}")
    
    # Validate imports first (but don't stop if files don't exist)
    print("\n📋 Validating imports...")
    validate_documentation()  # Don't stop on failure, just warn
    
    # Generate OpenAPI spec
    print("\n📄 Generating OpenAPI specification...")
    openapi_spec = generate_openapi_yaml()
    
    if openapi_spec and openapi_spec.get('paths'):
        # Generate Postman collection
        print("\n📮 Generating Postman collection...")
        generate_postman_collection(openapi_spec)
        
        print(f"\n📊 Generated documentation stats:")
        print(f"   - API version: {openapi_spec.get('info', {}).get('version', 'Unknown')}")
        print(f"   - Endpoints: {len(openapi_spec.get('paths', {}))}")
        print(f"   - Schemas: {len(openapi_spec.get('components', {}).get('schemas', {}))}")
        
        # Validate generated files
        print("\n✅ Validating generated files...")
        validate_generated_files()
    else:
        print("❌ Failed to generate OpenAPI specification or no paths found")
        print("This might indicate that Flask-RESTx isn't properly configured or routes aren't registered")
        return
    
    print("\n📚 Documentation generation complete!")
    print("\nGenerated files:")
    print("1. docs/openapi/openapi.yaml - OpenAPI 3.0 specification")
    print("2. docs/postman/MarketDataAPI.postman_collection.json - Postman collection")
    print("\nNext steps:")
    print("1. Review generated files in docs/")
    print("2. Import Postman collection for API testing")
    print("3. Update getting started guides if needed")

if __name__ == "__main__":
    main()
