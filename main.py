# from segmenter import pick_possessions

if __name__ == '__main__':
    """
    ids = ['0021500316', '0021500270', '0021500149', '0021500197',
           '0021500428', '0021500350', '0021500336',
           '0021500476', '0021500582']
    # ids = ['0021500582']
    moments = []

    for id in ids:
        # acquire_pbp_json(id)
        moments += pick_possessions('data/pbp/' + id + 'pbp.json')
    print len(moments)
    """
    import json
    from segmenter.core import convert_moment_to_action
    from preprocessor.utils import transform_wlog
    testdata = json.load(open('data/sportvu/0021500582.json'))
    eid = 30  # 4
    action = convert_moment_to_action(testdata, eid)
    action = transform_wlog(action)
    print action
    from visualizer.actionvisualizer import run
    run(eid=eid, act=action)
