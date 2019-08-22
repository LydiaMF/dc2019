#  https://casaguides.nrao.edu/index.php/M100_Band3_Combine_5.4
#
#  The original M100 data, as described in the casaguide, are rather big (26 GB)
#
#  For various workshops we trim these down to a more manageable 70 channel 5km/s data set
#  But you can edit this file to trim it down even more. Sometimes referred to as the QAC benchmark
#  data, as it's used by the 2 minute tp2vis benchmark in QAC (cd QAC/test ; make bench)
#  An earlier version of the benchmark was based on CASA4 , but this script has been updated to
#  reflect a more modern CASA5. For sake of insanity, we kept the names the same. 


# Older data: ("CASA4")
#    wget https://bulk.cv.nrao.edu/almadata/sciver/M100Band3_12m/M100_Band3_12m_CalibratedData.tgz
#    wget https://bulk.cv.nrao.edu/almadata/sciver/M100Band3ACA/M100_Band3_7m_CalibratedData.tgz
#    wget https://bulk.cv.nrao.edu/almadata/sciver/M100Band3ACA/M100_Band3_ACA_ReferenceImages_4.3.tgz
# Newer data: ("CASA5")
#    wget https://bulk.cv.nrao.edu/almadata/sciver/M100Band3_12m/M100_Band3_12m_CalibratedData.tgz
#    wget https://bulk.cv.nrao.edu/almadata/sciver/M100Band3ACA/M100_Band3_7m_CalibratedData.tgz
#    wget https://bulk.cv.nrao.edu/almadata/sciver/M100Band3ACA/M100_Band3_ACA_ReferenceImages_5.1.tgz

#
#    tar xvfz M100_Band3_12m_CalibratedData.tgz
#    tar xvfz M100_Band3_7m_CalibratedData.tgz
#    tar xvfz M100_Band3_ACA_ReferenceImages_5.1.tgz
#
#    mv M100_Band3_12m_CalibratedData/M100_Band3_12m_CalibratedData.ms   .
#    mv M100_Band3_7m_CalibratedData/M100_Band3_7m_CalibratedData.ms     .
#    mv M100_Band3_ACA_ReferenceImages_5.1/M100_TP_CO_cube.spw3.image.bl .

#   we start with this from M100Band3...
ms1 = 'M100_Band3_12m_CalibratedData.ms'
ms2 = 'M100_Band3_7m_CalibratedData.ms'
tp1 = 'M100_TP_CO_cube.spw3.image.bl'

#   make sure they exist
QAC.assertf(ms1)
QAC.assertf(ms2)
QAC.assertf(tp1)

#   this is the spectral axis we want, given in the LSRK frame
line = {"restfreq":'115.271202GHz','start':'1400km/s', 'width':'5km/s','nchan':70}

#   and want these dataset names for the QAC benchmark

ms1q = 'M100_aver_12.ms'
ms2q = 'M100_aver_7.ms'
tp1q = 'M100_TP_CO_cube.bl.image'

#   this is the final product here
benchtar = 'qac_bench5.tar.gz'


#   to add to the challenge, the TP map has the highest frequency first, the MS files are lowest frequency first
#   generally tclean, if used with specmode='cube', does not like to combine these.

#qac_summary(tp1, [ms1,ms2])

os.system('rm -rf %s' % ms1q)
mstransform(ms1, ms1q,
            datacolumn='DATA',outframe='LSRK',mode='velocity',regridms=True,nspw=1,spw='0',field='M100',keepflags=False,
            **line)

os.system('rm -rf %s' % ms2q)
mstransform(ms2, ms2q,
            datacolumn='DATA',outframe='LSRK',mode='velocity',regridms=True,nspw=1,spw='3,5',field='M100',keepflags=False,
            **line)

# the M100_aver_12.ms dataset has a missing getcol::REST_FREQUENCY, the ones in the M100_aver_7.ms are wrong
if True:
    rf0 = 115.2712018e9         # this might be the more formal restfreq, but wasn't used
    rf0 = 115.271202e9          # (114.60024366825306, 114.73289732123453, 115.271202,  1744.9999999999588, 1399.9999999999975, -4.9999999999994396, 70)
    tb.open(ms1q + '/SOURCE', nomodify=False)
    rf = np.array([[rf0]]) 
    tb.putcol('REST_FREQUENCY', rf)
    tb.close()

    tb.open(ms2q + '/SOURCE', nomodify=False)
    rf = np.array([[rf0,rf0]]) 

    tb.putcol('REST_FREQUENCY', rf)
    tb.close()


os.system('rm -rf %s' % tp1q)
imtrans(tp1, tp1q, '012-3')


qac_summary(tp1q, [ms1q,ms2q])
qac_stats(ms1q,'1.1768639368547504 0.64537772802755577 0.00058940987456351226 7.0547655988877178 0.0')
qac_stats(ms2q,'2.5704516191133808 1.4169106044781279 0.0011036963438420227 15.982205689901765 0.0')
qac_stats(tp1q,'0.5993522068193684 1.3645259947183588 -0.72602438926696777 8.8048715591430664 3561.9630360887845')
          
os.system("tar zcf %s qac_bench5.tar.gz %s %s %s" % (benchtar,tp1q,ms1q,ms2q))

"""
4.3 has 56.8986 beam from the 4.3 reference images
5.1 has 56.9677 beam from the 5.1 reference images

4.3 -> M100_Band3_ACA_ReferenceImages/M100_TP_CO_cube.bl.image
5.1 -> M100_Band3_ACA_ReferenceImages_5.1/M100_TP_CO_cube.spw3.image.bl

QAC_STATS: M100_TP_CO_cube.bl.image      0.54682752152594571 1.2847112260328173 -0.89499807357788086 8.8632850646972656 4001.3152006372839 
QAC_STATS: M100_TP_CO_cube.spw3.image.bl 0.59935220681936829 1.3645259947183597 -0.72602438926696777 8.8048715591430664 3561.963036064973 

QAC_STATS: M100_TP_CO_cube.spw3.image.bl 0.59935220681936829 1.3645259947183597 -0.72602438926696777 8.8048715591430664 3561.963036064973 
QAC_STATS: M100_TP_CO_cube.bl.image 0.5993522068193684 1.3645259947183588 -0.72602438926696777 8.8048715591430664 3561.9630360887845 

Old 4.3:
QAC_STATS: M100_aver_12.ms 1.177256275796271 0.64576812715900356 0.00059684379497741192 7.0609529505808935 0.0 
QAC_STATS: M100_aver_7.ms 2.5714851372581906 1.4175336201556363 0.0011051818163008522 15.982229345769259 0.0 
QAC_STATS: M100_TP_CO_cube.bl.image/ 0.54682752152594571 1.2847112260328173 -0.89499807357788086 8.8632850646972656 4001.3152006372839
Sizes:
91136   M100_aver_12.ms
35404   M100_aver_7.ms
3516    M100_TP_CO_cube.bl.image

New 5.1:

Sizes:
91136   M100_aver_12.ms
35396   M100_aver_7.ms
2452    M100_TP_CO_cube.spw3.image.bl/


"""
