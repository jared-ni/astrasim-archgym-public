# astrasim-archgym

## Themis
To reproduce themis results, please use files under `./themis`. The inputs are at `./themis/inputs` and you can also run experiments in batch with scripts in `./themis/scripts`

## Customized knobs
In `./dse`, it provides some basic python scripts to construct the astrasim cfg file on your own. In `./dse/archgen_v1_knobs` shows an example generating cfgs with some of the fileds with smaller design space, while in `./dse/all_knobs/` shows an example of a cfg generator on all possible fields. 

The type/possible values of each field is defined at `./dse/all_available_knobs_spec.py`.
