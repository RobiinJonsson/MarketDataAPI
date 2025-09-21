import pytest
from ..schema.schema_mapper import SchemaMapper

@pytest.fixture
def sample_base_schema():
    return {
        "name": "test_base",
        "description": "Test base schema",
        "fields": [
            {
                "name": "identifier",
                "source": "isin",
                "type": "string",
                "required": True,
                "description": "ISIN identifier"
            }
        ]
    }

@pytest.fixture
def sample_extended_schema():
    return {
        "name": "test_extended",
        "description": "Test extended schema",
        "extends": "test_base",
        "fields": [
            {
                "name": "price",
                "source": "last_price",
                "type": "number",
                "required": False,
                "description": "Current price",
                "transformation": "round(2)"
            }
        ]
    }

class TestSchemaVersioning:
    def test_schema_creation(self, sample_base_schema):
        """Test creating a new schema"""
        mapper = SchemaMapper()
        mapper.add_schema(sample_base_schema)
        
        version, schema = mapper.get_schema_version("test_base")
        assert version == "1.0"
        assert schema.name == "test_base"
        assert len(schema.fields) == 1

    def test_schema_update(self, sample_base_schema):
        """Test updating existing schema creates new version"""
        mapper = SchemaMapper()
        mapper.add_schema(sample_base_schema)
        
        # Update schema with new field
        updated_schema = sample_base_schema.copy()
        updated_schema["fields"].append({
            "name": "currency",
            "source": "currency",
            "type": "string",
            "required": False,
            "description": "Currency code"
        })
        
        mapper.update_schema("test_base", updated_schema)
        version, schema = mapper.get_schema_version("test_base")
        assert version == "1.1"
        assert len(schema.fields) == 2

    def test_schema_inheritance(self, sample_base_schema, sample_extended_schema):
        """Test schema inheritance and dependency tracking"""
        mapper = SchemaMapper()
        mapper.add_schema(sample_base_schema)
        mapper.add_schema(sample_extended_schema)
        
        # Check dependencies
        assert mapper.has_dependents("test_base")
        fields = mapper.get_schema_fields("test_extended")
        assert len(fields) == 2  # Should have both base and extended fields

    def test_schema_versioning(self, sample_base_schema):
        """Test version history tracking"""
        mapper = SchemaMapper()
        mapper.add_schema(sample_base_schema)
        
        # Create multiple versions
        for i in range(2):
            updated = sample_base_schema.copy()
            updated["description"] = f"Version {i+2}"
            mapper.update_schema("test_base", updated)
        
        versions = mapper.get_schema_versions("test_base")
        assert len(versions) == 3  # Original + 2 updates
        assert versions[0]["version"] == "1.0"
        assert versions[-1]["version"] == "1.2"

    def test_safe_schema_deletion(self, sample_base_schema, sample_extended_schema):
        """Test schema deletion with dependency checks"""
        mapper = SchemaMapper()
        mapper.add_schema(sample_base_schema)
        mapper.add_schema(sample_extended_schema)
        
        # Should not be able to delete base schema while it has dependents
        with pytest.raises(ValueError):
            mapper.delete_schema("test_base")
        
        # Should be able to delete extended schema
        mapper.delete_schema("test_extended")
        assert not mapper.has_dependents("test_base")

    def test_version_retrieval(self, sample_base_schema):
        """Test retrieving specific schema versions"""
        mapper = SchemaMapper()
        mapper.add_schema(sample_base_schema)
        
        # Create new version
        updated = sample_base_schema.copy()
        updated["description"] = "Updated version"
        mapper.update_schema("test_base", updated)
        
        # Get specific versions
        v1_schema = mapper.get_schema_by_version("test_base", "1.0")
        v2_schema = mapper.get_schema_by_version("test_base", "1.1")
        
        assert v1_schema.description == "Test base schema"
        assert v2_schema.description == "Updated version"
