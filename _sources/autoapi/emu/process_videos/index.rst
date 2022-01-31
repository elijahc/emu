:py:mod:`emu.process_videos`
============================

.. py:module:: emu.process_videos


Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   emu.process_videos.add_start
   emu.process_videos.add_end
   emu.process_videos.process_video
   emu.process_videos.process
   emu.process_videos.preprocess



Attributes
~~~~~~~~~~

.. autoapisummary::

   emu.process_videos.trickshots
   emu.process_videos.records
   emu.process_videos.resolution_presets
   emu.process_videos.get_url_params


.. py:data:: trickshots
   

   

.. py:data:: records
   

   

.. py:data:: resolution_presets
   

   

.. py:data:: get_url_params
   

   

.. py:function:: add_start(df)


.. py:function:: add_end(df)


.. py:function:: process_video(in_file, out_file=None, suffix=None, verbose=True, audio_bitrate='128k', video_bitrate='750k', preset='slow', **kwargs)


.. py:function:: process(infile, resolution, start=0, end=None, video_set=None, video_directory=None, verbose=False)


.. py:function:: preprocess(*args, **kwargs)


