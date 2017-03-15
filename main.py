# from segmenter import pick_possessions

if __name__ == '__main__':
    """
    from playbyplay.utils import acquire_pbp_json
    ids = ['0021500316', '0021500270', '0021500149', '0021500197',
           '0021500428', '0021500350', '0021500336',
           '0021500476', '0021500582']
    # ids = ['0021500582']
    moments = []

    for id in ids:
        acquire_pbp_json(id)
        # moments += pick_possessions('data/pbp/' + id + 'pbp.json')
    print len(moments)
    """

    """
    import json
    from segmenter.core import convert_moment_to_action
    testdata = json.load(open('data/sportvu/0021500582.json'))
    eid = 139  # 30  # 4
    action = convert_moment_to_action(testdata, eid)
    print action
    from visualizer.actionvisualizer import run
    run(eid=eid, act=action)
    """

    """
    from action.core import load_action
    from preprocessor.utils import determine_matchup
    from frameone import run as fr_run
    eid = 139
    action = load_action("0021500582", eid)

    from preprocessor.features import get_entropy, get_mean_distance
    import numpy as np
    entropy = get_entropy(action)

    print "event id: " + str(eid)
    print "avg entropy: " + str(np.mean(entropy))
    print entropy

    mean_dist = get_mean_distance(action)
    print "avg dist: " + str(np.mean(mean_dist))
    print mean_dist

    # fr_run(eid=eid)
    # """

    # canonical = 0.423526057228446
    # distance  = 0.72332673966884609

    from eda.matchups import count_matchup_over_time
    # count_matchup_over_time(eid=eid, by="canonical")
