import os
import sys
from utils.pipeline_aux import check_initial_path
from dlib_predictor import main_for_generic_detector
from ffld2 import main_for_ps_detector
from ps_pbaam import main_for_ps_aam
from visualise_landmarks import main_call_visualisations
from visualisations_to_videos import main_call_visualisation_to_videos

s = os.path.sep  # OS separator

#######################################################
#######################################################
##############   folders for landmarks   ##############
s_1 = '1_detect' + s
s_1_pr = '1_pred' + s
s_2 = '2_psd' + s
s_3 = '3_ffld_ln' + s
s_4 = '4_pbaam' + s
s_5 = '5_svm' + s
s_6 = '6_pbaam' + s
s_7 = '7_svm_faces' + s
#######################################################
#######################################################


def run_main(path_clips):
    # Step 1: Generic detector
    main_for_generic_detector(path_clips, s_1, s_1_pr)
    # Step 2: Person specific detector (train and apply)
    main_for_ps_detector(path_clips, s_1, s_2, s_2[:-1] + '_models' + s, s_3)
    # Step 3: Person specific (part-based) AAM
    main_for_ps_aam(path_clips, s_3, s_4, s_4[:-1] + '_models' + s, out_ln_svm=s_5,
                    n_shape=[3, 12], n_appearance=[50, 100])
    # Step 4: (loop) Person specific AAM
    main_for_ps_aam(path_clips, s_5, s_6, s_6[:-1] + '_models' + s, loop=True,
                    d_aam=180, max_helen=400, max_cl_e=100, in_ln_fit_fol=s_4,
                    mi=250, n_shape=[5, 13], n_appearance=[50, 100], out_ln_svm=s_7)
    # TODO: Add tests for the steps.
    # Visualise landmarks
    main_call_visualisations(path_clips, [s_7, s_1], 'visualise')
    # Convert the visualisations to videos
    main_call_visualisation_to_videos(path_clips, False)

if __name__ == '__main__':
    args = len(sys.argv)
    path_clips_m = check_initial_path(args, sys.argv)
    run_main(path_clips_m)
