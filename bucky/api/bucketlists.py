from flask import jsonify, request, g, url_for
from authentication import auth
from bucky import db
from bucky.models import BucketList
from errors import forbidden, bad_request


def register_routes(api):
    @api.route('/bucketlists/<int:bucketlist_id>')
    @auth.login_required
    def get_bucketlist(bucketlist_id):
        bucketlist = BucketList.query.get_or_404(bucketlist_id)
        return jsonify(bucketlist.to_json())

    @api.route('/bucketlists')
    @auth.login_required
    def get_bucketlists():
        query = request.args['q'] if 'q' in request.args else None
        limit = request.args['limit'] if 'limit' in request.args else 20

        # make sure limit does not exceed 100
        if int(limit) > 100:
            return bad_request("Maximum Pagination Limit Exceeded.")
        if query is not None:
            bucketlists = BucketList.query.filter(
                BucketList.created_by == g.current_user.id,
                BucketList.title.like('%' + query + '%')
            )
        else:
            bucketlists = BucketList.query.filter_by(
                    created_by=g.current_user.id).limit(limit).all()

        return jsonify([bucketlist.to_json() for bucketlist in bucketlists])

    @api.route('/bucketlists', methods=['POST'])
    @auth.login_required
    def new_bucketlist():
        bucketlist = BucketList.from_json(request.json)
        bucketlist.created_by = g.current_user.id
        db.session.add(bucketlist)
        db.session.commit()
        return jsonify({
            'message': 'Bucketlist created successfully.',
            'Location': url_for(
                            'api.get_bucketlist',
                            bucketlist_id=bucketlist.id,
                            _external=True,
                        )
        }), 201

    @api.route('/bucketlists/<int:bucketlist_id>', methods=['PUT'])
    @auth.login_required
    def edit_bucketlist(bucketlist_id):
        bucketlist = BucketList.query.get_or_404(bucketlist_id)
        if g.current_user.id != bucketlist.created_by:
            return forbidden('Access to resource forbidden.')

        if request.json.get('title'):
            bucketlist.title = request.json.get('title')

        if request.json.get('description'):
            bucketlist.description = request.json.get('description')

        db.session.add(bucketlist)
        db.session.commit()

        return jsonify({
            'message': 'Bucketlist updated successfully.',
            'Location': url_for(
                            'api.get_bucketlist',
                            bucketlist_id=bucketlist.id,
                            _external=True,
                        )
        }), 200

    @api.route('/bucketlists/<int:bucketlist_id>', methods=['DELETE'])
    @auth.login_required
    def delete_bucketlist(bucketlist_id):
        bucketlist = BucketList.query.get_or_404(bucketlist_id)
        if g.current_user.id != bucketlist.created_by:
            return forbidden('Access to resource forbidden.')
        db.session.delete(bucketlist)
        db.session.commit()
        return ('', 204)
