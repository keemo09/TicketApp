from marshmallow import Schema, fields, validates_schema, ValidationError

class PrizeSchema(Schema):
    product_name = fields.Str(required=True, error_messages={"required": "product_name is required."})
    product_description = fields.Str(required=False, error_messages={"required": "product_name is required."})


class CampaignSchema(Schema):
    name = fields.Str(required=True, error_messages={"required": "Name of campaign is required."})
    end_date = fields.DateTime(required=True, error_messages={"required": "end_date is required."})
    max_ticket = fields.Int(required=True, error_messages={"required": "max_ticket is required."})

    # Nestet validation
    prizes = fields.List(fields.Nested(PrizeSchema), required=True, error_messages={"required": "Prizes are required."})

    @validates_schema
    def validate_prizes(self, data, **kwargs):
        if not data['prizes']:
            raise ValidationError("Prizes list cannot be empty.", field_name="prizes")