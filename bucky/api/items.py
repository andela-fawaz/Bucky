from flask import jsonify, request, g, url_for
from .. import db
from ..models import BucketList, Item
from .authentication import auth
from .errors import forbidden


def register_routes(api):

    @api.route('/bucketlists/<int:bucketlist_id>/items/<int:item_id>')
    @auth.login_required
    def get_bucketlist_item(bucketlist_id, item_id):
        bucketlist = BucketList.query.get_or_404(bucketlist_id)
        item = bucketlist.items.filter_by(id=item_id).first_or_404()

        return jsonify(item.to_json())

    @api.route('/bucketlists/<int:bucketlist_id>/items')
    @auth.login_required
    def get_bucketlist_items(bucketlist_id):
        bucketlist = BucketList.query.get_or_404(bucketlist_id)
        items = bucketlist.items.all()
        return jsonify([item.to_json() for item in items])

    @api.route('/bucketlists/<int:bucketlist_id>/items', methods=['POST'])
    @auth.login_required
    def add_bucketlist_item(bucketlist_id):
        bucketlist = BucketList.query.get_or_404(bucketlist_id)
        if g.current_user.id != bucketlist.created_by:
            return forbidden('Access to resource forbidden.')
        item = Item.from_json(request.json)
        item.bucketlist = bucketlist
        db.session.add(item)
        db.session.commit()
        return jsonify({
            'message': 'Item successfully added in bucketlist.',
            'Location': url_for(
                'api.get_bucketlist_item',
                bucketlist_id=bucketlist.id,
                item_id=item.id,
                _external=True,
            )
        }), 201

    @api.route('/bucketlists/<int:bucketlist_id>/items/<int:item_id>',
               methods=['PUT'])
    @auth.login_required
    def edit_bucketlist_item(bucketlist_id, item_id):
        bucketlist = BucketList.query.get_or_404(bucketlist_id)
        if g.current_user.id != bucketlist.created_by:
            return forbidden('Access to resource forbidden.')

        item = bucketlist.items.filter_by(id=item_id).first_or_404()

        item.title = request.json.get('title')
        item.description = request.json.get('description')

        db.session.add(item)
        db.session.commit()

        return jsonify({
            'message': 'Item updated successfully.',
            'Location': url_for(
                            'api.get_bucketlist_item',
                            bucketlist_id=bucketlist.id,
                            item_id=item.id,
                            _external=True,
                        )
        }), 200

    @api.route('/bucketlists/<int:bucketlist_id>/items/<int:item_id>',
               methods=['DELETE'])
    @auth.login_required
    def delete_bucketlist_item(bucketlist_id, item_id):
        bucketlist = BucketList.query.get_or_404(bucketlist_id)
        if g.current_user.id != bucketlist.created_by:
            return forbidden('Access to resource forbidden.')
        item = bucketlist.items.filter_by(id=item_id).first_or_404()
        db.session.delete(item)
        db.session.commit()
        return ('', 204)
