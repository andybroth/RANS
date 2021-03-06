      subroutine xpand (xx)
c
c     ******************************************************************
c     *                                                                *
c     *   generates a coarser mesh by taking alternate points          *
c     *                                                                *
c     ******************************************************************
c
      use dims
      use dimsc
c
c     ******************************************************************
c
      use mesh_var
c
c     ******************************************************************
c
      implicit none
c
c     ******************************************************************
c
      real, dimension(iil,jjl,2)           :: xx
c
c     ******************************************************************
c
c     local variables
c
c     ******************************************************************
c
      integer  :: i,j,ii,jj
c
c     ******************************************************************
c
         jj        = 0
      do j=1,jl,2
         jj        = jj  +1
         ii        = 0
      do i=1,il,2
         ii        = ii  +1
         xx(ii,jj,1)  = x(i,j,1)
         xx(ii,jj,2)  = x(i,j,2)
      end do
      end do

      return

      end
