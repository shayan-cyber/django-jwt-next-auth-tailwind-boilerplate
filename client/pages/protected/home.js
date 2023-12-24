import React from 'react'
import { useSession } from 'next-auth/react'
function home() {
    const session  = useSession();
  console.log(session);
  return (
    <div>home</div>
  )
}

export default home