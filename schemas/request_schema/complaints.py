from marshmallow import Schema, fields


class ComplaintRequestSchema(Schema):
    title = fields.Str(Required=True)
    description = fields.Str(Required=True)
    photo_url = fields.Str(Required=True)
    amount = fields.Float(Required=True)
    
