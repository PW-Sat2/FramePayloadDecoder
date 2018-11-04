from payload_decoder import PayloadDecoder
import pprint


raw_frame_payload = open('example_frames/telemetry_frame_payload.bin', 'rb').read()
pprint.pprint(PayloadDecoder.decode(raw_frame_payload))

raw_frame_payload = open('example_frames/periodic_frame_payload.bin', 'rb').read()
pprint.pprint(PayloadDecoder.decode(raw_frame_payload))

raw_frame_payload = open('example_frames/file_list_frame_payload.bin', 'rb').read()
pprint.pprint(PayloadDecoder.decode(raw_frame_payload))
