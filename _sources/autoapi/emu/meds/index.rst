:py:mod:`emu.meds`
==================

.. py:module:: emu.meds


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   emu.meds.DrugAdministration
   emu.meds.Drug
   emu.meds.Levetiracetam
   emu.meds.Lacosamide
   emu.meds.Lamotrigine
   emu.meds.Pregabalin



Functions
~~~~~~~~~

.. autoapisummary::

   emu.meds.gen_norm_dist



.. py:function:: gen_norm_dist(clip_a, clip_b, u=None)


.. py:class:: DrugAdministration(drug, doses, times, weight)

   .. py:method:: Vd(self)
      :property:


   .. py:method:: CL(self)
      :property:


   .. py:method:: Tmax(self)
      :property:


   .. py:method:: set_baseline(self, dose, interval)


   .. py:method:: Css(self, dose, interval)


   .. py:method:: u(self, t)


   .. py:method:: C(self, t, normalize=False)


   .. py:method:: plot(self)


   .. py:method:: plot_Cp(self, span=25, C0=0, normalize=False)



.. py:class:: Drug

   Bases: :py:obj:`object`

   .. py:attribute:: _weight
      :annotation: = 80

      

   .. py:method:: get_CL(self, wt=80)


   .. py:method:: show_Vd(self, wt=None)


   .. py:method:: show_CL(self, wt=None)


   .. py:method:: __str__(cls)
      :classmethod:

      Return str(self).



.. py:class:: Levetiracetam

   Bases: :py:obj:`Drug`

   .. py:attribute:: _name_
      :annotation: = Levetiracetam

      

   .. py:attribute:: F
      :annotation: = 0.96

      

   .. py:attribute:: _Vd
      :annotation: = 0.7

      

   .. py:attribute:: _CL
      

      

   .. py:attribute:: _Tmax
      :annotation: = 1.5

      

   .. py:method:: create_administration(cls, doses, times, weight)
      :classmethod:



.. py:class:: Lacosamide

   Bases: :py:obj:`Drug`

   .. py:attribute:: _name_
      :annotation: = Lacosamide

      

   .. py:attribute:: F
      :annotation: = 1.0

      

   .. py:attribute:: CL_dist
      

      

   .. py:attribute:: Tmax_dist
      

      

   .. py:attribute:: _Vd
      :annotation: = 0.6

      

   .. py:attribute:: _CL
      

      

   .. py:attribute:: _Tmax
      

      

   .. py:method:: create_administration(cls, doses, times, weight)
      :classmethod:



.. py:class:: Lamotrigine

   Bases: :py:obj:`Drug`

   .. py:attribute:: _name_
      :annotation: = Lamotrigine

      

   .. py:attribute:: F
      :annotation: = 0.98

      

   .. py:attribute:: CL_dist
      

      

   .. py:attribute:: Tmax_dist
      

      

   .. py:attribute:: Vd_dist
      

      

   .. py:attribute:: _Vd
      

      

   .. py:attribute:: _CL
      

      

   .. py:attribute:: _Tmax
      

      

   .. py:method:: create_administration(cls, doses, times, weight)
      :classmethod:



.. py:class:: Pregabalin

   Bases: :py:obj:`Drug`

   .. py:attribute:: _name_
      :annotation: = Pregabalin

      

   .. py:attribute:: F
      :annotation: = 0.95

      

   .. py:attribute:: CL_dist
      

      

   .. py:attribute:: _Vd
      :annotation: = 0.5

      

   .. py:attribute:: _CL
      

      

   .. py:attribute:: _Tmax
      :annotation: = 1.5

      

   .. py:method:: create_administration(cls, doses, times, weight)
      :classmethod:


   .. py:method:: show_CL(cls, wt=None)
      :classmethod:


   .. py:method:: get_CL(cls, wt=80)
      :classmethod:



